"""
Author: Eric J. Ma
License: MIT

A Python module that computes the protein interaction graph from a PDB file.
"""

from collections import defaultdict
from itertools import combinations

import networkx as nx
import numpy as np
import pandas as pd
from scipy.spatial import Delaunay
from scipy.spatial.distance import euclidean, pdist, squareform
from sklearn.preprocessing import LabelBinarizer

from .resi_atoms import (
    AA_RING_ATOMS,
    AROMATIC_RESIS,
    BACKBONE_ATOMS,
    BOND_TYPES,
    CATION_PI_RESIS,
    CATION_RESIS,
    DISULFIDE_ATOMS,
    DISULFIDE_RESIS,
    HYDROPHOBIC_RESIS,
    IONIC_RESIS,
    ISOELECTRIC_POINTS_STD,
    MOLECULAR_WEIGHTS_STD,
    NEG_AA,
    PI_RESIS,
    POS_AA,
    RESI_NAMES,
)


class ProteinGraph(nx.Graph):
    """
    The ProteinGraph object.

    Inherits from the NetworkX Graph object.

    Implements further functions for automatically computing the graph
    structure.

    Certain functions are available for integration with the
    neural-fingerprint Python package.
    """

    def __init__(self, pdb_handle):
        super(ProteinGraph, self).__init__()
        self.pdb_handle = pdb_handle
        self.dataframe = self.parse_pdb()
        self.compute_chain_pos_aa_mapping()

        # Mapping of chain -> position -> aa
        self.distmat = self.compute_distmat(self.dataframe)
        self.rgroup_df = self.get_rgroup_dataframe_()
        # Automatically compute the interaction graph upon loading.
        self.compute_interaction_graph()
        self.compute_all_node_features()
        self.compute_all_edge_features()

        # Convert all metadata that are set datatypes to lists.
        self.convert_all_sets_to_lists()

    def compute_chain_pos_aa_mapping(self):
        """Computes the mapping: chain -> position -> aa"""
        self.chain_pos_aa = defaultdict(dict)
        for (chain, pos, aa), d in self.dataframe.groupby(
            ["chain_id", "resi_num", "resi_name"]
        ):
            self.chain_pos_aa[chain][pos] = aa

    def convert_all_sets_to_lists(self):
        for n, d in self.nodes(data=True):
            for k, v in d.items():
                if isinstance(v, set):
                    self.node[n][k] = [i for i in v]

        for u1, u2, d in self.edges(data=True):
            for k, v in d.items():
                if isinstance(v, set):
                    self.edges[u1, u2][k] = [i for i in v]

    def compute_interaction_graph(self):
        """
        Computes the interaction graph.

        Graph definition and metadata:
        ==============================
        - Node: Amino acid position.
            - aa: amino acid identity

        - Edge: Any interaction found by the atomic interaction network.
            - hbond:            BOOLEAN
            - disulfide:        BOOLEAN
            - hydrophobic:      BOOLEAN
            - ionic:            BOOLEAN
            - aromatic:         BOOLEAN
            - aromatic_sulphur: BOOLEAN
            - cation_pi:        BOOLEAN
        """
        # Add in nodes with their metadata
        # Metadata are:
        # - x, y, z coordinates of C-alpha
        # - chain_id
        # - resi_num
        # - resi_name
        for g, d in self.dataframe.query("record_name == 'ATOM'").groupby(
            ["node_id", "chain_id", "resi_num", "resi_name"]
        ):
            node_id, chain_id, resi_num, resi_name = g
            x = d.query("atom == 'CA'")["x"].values[0]
            y = d.query("atom == 'CA'")["y"].values[0]
            z = d.query("atom == 'CA'")["z"].values[0]
            self.add_node(
                node_id,
                chain_id=chain_id,
                resi_num=resi_num,
                resi_name=resi_name,
                x=x,
                y=y,
                z=z,
                features=None,
            )

        # Add in edges for amino acids that are adjacent in the linear amino
        # acid sequence.
        for n, d in self.nodes(data=True):
            chain = d["chain_id"]
            pos = d["resi_num"]
            aa = d["resi_name"]

            if pos - 1 in self.chain_pos_aa[chain].keys():
                prev_aa = self.chain_pos_aa[chain][pos - 1]
                prev_node = f"{chain}{pos-1}{prev_aa}"
                if aa in RESI_NAMES and prev_aa in RESI_NAMES:
                    self.add_edge(n, prev_node, kind={"backbone"})

            if pos + 1 in self.chain_pos_aa[chain].keys():
                next_aa = self.chain_pos_aa[chain][pos + 1]
                next_node = f"{chain}{pos+1}{next_aa}"
                if aa in RESI_NAMES and next_aa in RESI_NAMES:
                    self.add_edge(n, next_node, kind={"backbone"})

            # prev_node = d["chain_id"] + str(d["resi_num"] - 1)
            # next_node = d["chain_id"] + str(d["resi_num"] + 1)

            # Find the previous node in the graph.
            # prev_node = [n for n in self.nodes() if prev_node in n]
            # next_node = [n for n in self.nodes() if next_node in n]

            # if len(prev_node) == 1:
            # self.add_edge(n, prev_node[0], kind={"backbone"})

            # if len(next_node) == 1:
            # self.add_edge(n, next_node[0], kind={"backbone"})

        # Define function shortcuts for each of the interactions.
        funcs = dict()
        funcs["hydrophobic"] = self.add_hydrophobic_interactions_
        funcs["disulfide"] = self.add_disulfide_interactions_
        funcs["hbond"] = self.add_hydrogen_bond_interactions_
        funcs["ionic"] = self.add_ionic_interactions_
        funcs["aromatic"] = self.add_aromatic_interactions_
        funcs["aromatic_sulphur"] = self.add_aromatic_sulphur_interactions_
        funcs["cation_pi"] = self.add_cation_pi_interactions_
        # funcs['delaunay'] = self.add_delaunay_triangulation_

        # Add in each type of edge, based on the above.
        for k, v in funcs.items():
            v()

    def parse_pdb(self):
        """
        Parses the PDB file as a pandas DataFrame object.

        Backbone chain atoms are ignored for the calculation
        of interacting residues.
        """
        atomic_data = []
        with open(self.pdb_handle, "r") as f:
            for line in f.readlines():
                data = dict()
                if line[0:7].strip(" ") in ["ATOM", "HETATM"]:

                    data["record_name"] = line[0:7].strip(" ")
                    data["serial_number"] = int(line[6:11].strip(" "))
                    data["atom"] = line[12:15].strip(" ")
                    data["resi_name"] = line[17:20]
                    data["chain_id"] = line[21]
                    data["resi_num"] = int(line[23:26])
                    data["x"] = float(line[30:37])
                    data["y"] = float(line[38:45])
                    data["z"] = float(line[46:53])

                    atomic_data.append(data)

        atomic_df = pd.DataFrame(atomic_data)
        atomic_df["node_id"] = (
            atomic_df["chain_id"]
            + atomic_df["resi_num"].map(str)
            + atomic_df["resi_name"]
        )

        return atomic_df

    def compute_distmat(self, dataframe):
        """
        Computes the pairwise euclidean distances between every atom.

        Design choice: passed in a DataFrame to enable easier testing on
        dummy data.
        """

        self.eucl_dists = pdist(dataframe[["x", "y", "z"]], metric="euclidean")
        self.eucl_dists = pd.DataFrame(squareform(self.eucl_dists))
        self.eucl_dists.index = dataframe.index
        self.eucl_dists.columns = dataframe.index

        return self.eucl_dists

    def get_interacting_atoms_(self, angstroms, distmat):
        """
        Finds the atoms that are within a particular radius of one another.
        """
        return np.where(distmat <= angstroms)

    def add_interacting_resis_(self, interacting_atoms, dataframe, kind):
        """
        Returns a list of 2-tuples indicating the interacting residues based
        on the interacting atoms. This is most typically called after the
        get_interacting_atoms_ function above.

        Also filters out the list such that the residues have to be at least
        two apart.

        Parameters:
        ===========
        - interacting_atoms:    (numpy array) result from
                                get_interacting_atoms_ function.
        - dataframe:            (pandas dataframe) a pandas dataframe that
                                houses the euclidean locations of each atom.
        - kind:                 (list) the kind of interaction. Contains one
                                of :
                                - hydrophobic
                                - disulfide
                                - hbond
                                - ionic
                                - aromatic
                                - aromatic_sulphur
                                - cation_pi
                                - delaunay

        Returns:
        ========
        - filtered_interacting_resis: (set of tuples) the residues that are in
                                      an interaction, with the interaction kind
                                      specified

        """
        # This assertion/check is present for defensive programming!
        for k in kind:
            assert k in BOND_TYPES

        resi1 = dataframe.loc[interacting_atoms[0]]["node_id"].values
        resi2 = dataframe.loc[interacting_atoms[1]]["node_id"].values

        interacting_resis = set(list(zip(resi1, resi2)))
        for i1, i2 in interacting_resis:
            if i1 != i2:
                if self.has_edge(i1, i2):
                    for k in kind:
                        self.edges[i1, i2]["kind"].add(k)
                else:
                    self.add_edge(i1, i2, kind=set(kind))

        # return filtered_interacting_resis

    def get_rgroup_dataframe_(self):
        """
        Returns just the atoms that are amongst the R-groups and not part of
        the backbone chain.
        """

        rgroup_df = self.filter_dataframe(
            self.dataframe, "atom", BACKBONE_ATOMS, False
        )
        return rgroup_df

    def filter_dataframe(self, dataframe, by_column, list_of_values, boolean):
        """
        Filters the [dataframe] such that the [by_column] values have to be
        in the [list_of_values] list if boolean == True, or not in the list
        if boolean == False
        """
        df = dataframe.copy()
        df = df[df[by_column].isin(list_of_values) == boolean]
        df.reset_index(inplace=True, drop=True)

        return df

    # SPECIFIC INTERACTION FUNCTIONS #
    def add_hydrophobic_interactions_(self):
        """
        Finds all hydrophobic interactions between the following residues:
        ALA, VAL, LEU, ILE, MET, PHE, TRP, PRO, TYR

        Criteria: R-group residues are within 5A distance.
        """
        hydrophobics_df = self.filter_dataframe(
            self.rgroup_df, "resi_name", HYDROPHOBIC_RESIS, True
        )
        distmat = self.compute_distmat(hydrophobics_df)
        interacting_atoms = self.get_interacting_atoms_(5, distmat)
        self.add_interacting_resis_(
            interacting_atoms, hydrophobics_df, ["hydrophobic"]
        )

    def add_disulfide_interactions_(self):
        """
        Finds all disulfide interactions between CYS residues, such that the
        sulfur atom pairs are within 2.2A of each other.
        """

        disulfide_df = self.filter_dataframe(
            self.rgroup_df, "resi_name", DISULFIDE_RESIS, True
        )
        disulfide_df = self.filter_dataframe(
            disulfide_df, "atom", DISULFIDE_ATOMS, True
        )
        distmat = self.compute_distmat(disulfide_df)
        interacting_atoms = self.get_interacting_atoms_(2.2, distmat)
        self.add_interacting_resis_(
            interacting_atoms, disulfide_df, ["disulfide"]
        )

    def add_hydrogen_bond_interactions_(self):
        """
        Finds all hydrogen-bond interactions between atoms capable of hydrogen
        bonding.
        """
        # For these atoms, find those that are within 3.5A of one another.
        HBOND_ATOMS = [
            "ND",
            "NE",
            "NH",
            "NZ",
            "OD",
            "OE",
            "OG",
            "OH",
            "SD",
            "SG",
            "N",
            "O",
        ]
        hbond_df = self.filter_dataframe(
            self.rgroup_df, "atom", HBOND_ATOMS, True
        )
        distmat = self.compute_distmat(hbond_df)
        interacting_atoms = self.get_interacting_atoms_(3.5, distmat)
        self.add_interacting_resis_(interacting_atoms, hbond_df, ["hbond"])

        # For these atoms, find those that are within 4.0A of one another.
        HBOND_ATOMS_SULPHUR = ["SD", "SG"]
        hbond_df = self.filter_dataframe(
            self.rgroup_df, "atom", HBOND_ATOMS_SULPHUR, True
        )
        distmat = self.compute_distmat(hbond_df)
        interacting_atoms = self.get_interacting_atoms_(4.0, distmat)
        self.add_interacting_resis_(interacting_atoms, hbond_df, ["hbond"])

    def add_delaunay_triangulation_(self):
        """
        Computes the Delaunay triangulation of the protein structure.

        This has been used in prior work. References:
        - Harrison, R. W., Yu, X. & Weber, I. T. Using triangulation to include
          target structure improves drug resistance prediction accuracy. in 1–1
          (IEEE, 2013). doi:10.1109/ICCABS.2013.6629236
        - Yu, X., Weber, I. T. & Harrison, R. W. Prediction of HIV drug
          resistance from genotype with encoded three-dimensional protein
          structure. BMC Genomics 15 Suppl 5, S1 (2014).

        Notes:
        1. We do not use the add_interacting_resis function, because this
           interaction is computed on the CA atoms. Therefore, there is code
           duplication. For now, I have chosen to leave this code duplication
           in.
        """
        ca_coords = self.dataframe[self.dataframe["atom"] == "CA"]

        tri = Delaunay(ca_coords[["x", "y", "z"]])  # this is the triangulation
        for simplex in tri.simplices:
            nodes = ca_coords.reset_index().loc[simplex, "node_id"]

            for n1, n2 in combinations(nodes, 2):
                if self.has_edge(n1, n2):
                    self.edges[n1, n2]["kind"].add("delaunay")
                else:
                    self.add_edge(n1, n2, kind={"delaunay"})

    def add_ionic_interactions_(self):
        """
        Finds all ionic interactiosn between ARG, LYS, HIS, ASP, and GLU.
        Distance cutoff: 6A.
        """
        ionic_df = self.filter_dataframe(
            self.rgroup_df, "resi_name", IONIC_RESIS, True
        )
        distmat = self.compute_distmat(ionic_df)
        interacting_atoms = self.get_interacting_atoms_(6, distmat)

        self.add_interacting_resis_(interacting_atoms, ionic_df, ["ionic"])

        # Check that the interacting residues are of opposite charges
        for r1, r2 in self.get_edges_by_bond_type("ionic"):
            condition1 = (
                self.node[r1]["resi_name"] in POS_AA
                and self.node[r2]["resi_name"] in NEG_AA
            )

            condition2 = (
                self.node[r2]["resi_name"] in POS_AA
                and self.node[r1]["resi_name"] in NEG_AA
            )

            if not condition1 or condition2:
                self.edges[r1, r2]["kind"].remove("ionic")
                if len(self.edges[r1, r2]["kind"]) == 0:
                    self.remove_edge(r1, r2)

    def add_aromatic_interactions_(self):
        """
        Finds all aromatic-aromatic interactions by looking for phenyl ring
        centroids separated between 4.5A to 7A.

        Phenyl rings are present on PHE, TRP, HIS and TYR.

        Phenyl ring atoms on these amino acids are defined by the following
        atoms:
        - PHE: CG, CD, CE, CZ
        - TRP: CD, CE, CH, CZ
        - HIS: CG, CD, ND, NE, CE
        - TYR: CG, CD, CE, CZ

        Centroids of these atoms are taken by taking:
            (mean x), (mean y), (mean z)
        for each of the ring atoms.

        Notes for future self/developers:
        - Because of the requirement to pre-compute ring centroids, we do not
          use the functions written above (filter_dataframe, compute_distmat,
          get_interacting_atoms), as they do not return centroid atom
          euclidean coordinates.
        """
        dfs = []
        for resi in AROMATIC_RESIS:
            resi_rings_df = self.get_ring_atoms_(self.dataframe, resi)
            resi_centroid_df = self.get_ring_centroids_(resi_rings_df)
            dfs.append(resi_centroid_df)

        aromatic_df = pd.concat(dfs)
        aromatic_df.sort_values(by="node_id", inplace=True)
        aromatic_df.reset_index(inplace=True, drop=True)

        distmat = self.compute_distmat(aromatic_df)
        distmat.set_index(aromatic_df["node_id"], inplace=True)
        distmat.columns = aromatic_df["node_id"]
        distmat = distmat[(distmat >= 4.5) & (distmat <= 7)].fillna(0)
        indices = np.where(distmat > 0)

        interacting_resis = []
        for i, (r, c) in enumerate(zip(indices[0], indices[1])):
            interacting_resis.append((distmat.index[r], distmat.index[c]))

        for i, (n1, n2) in enumerate(interacting_resis):
            assert self.node[n1]["resi_name"] in AROMATIC_RESIS
            assert self.node[n2]["resi_name"] in AROMATIC_RESIS
            if self.has_edge(n1, n2):
                self.edges[n1, n2]["kind"].add("aromatic")
            else:
                self.add_edge(n1, n2, kind={"aromatic"})

    def get_ring_atoms_(self, dataframe, aa):
        """
        A helper function for add_aromatic_interactions_.

        Gets the ring atoms from the particular aromatic amino acid.

        Parameters:
        ===========
        - dataframe: the dataframe containing the atom records.
        - aa: the amino acid of interest, passed in as 3-letter string.

        Returns:
        ========
        - dataframe: a filtered dataframe containing just those atoms from the
                     particular amino acid selected. e.g. equivalent to
                     selecting just the ring atoms from a particular amino
                     acid.
        """

        ring_atom_df = self.filter_dataframe(
            dataframe, "resi_name", [aa], True
        )

        ring_atom_df = self.filter_dataframe(
            ring_atom_df, "atom", AA_RING_ATOMS[aa], True
        )
        return ring_atom_df

    def get_ring_centroids_(self, ring_atom_df):
        """
        A helper function for add_aromatic_interactions_.

        Computes the ring centroids for each a particular amino acid's ring
        atoms.

        Ring centroids are computed by taking the mean of the x, y, and z
        coordinates.

        Parameters:
        ===========
        - ring_atom_df: a dataframe computed using get_ring_atoms_.
        - aa: the amino acid under study

        Returns:
        ========
        - centroid_df: a dataframe containing just the centroid coordinates of
                       the ring atoms of each residue.
        """
        centroid_df = (
            ring_atom_df.groupby("node_id")
            .mean()[["x", "y", "z"]]
            .reset_index()
        )

        return centroid_df

    def add_aromatic_sulphur_interactions_(self):
        """
        Finds all aromatic-sulphur interactions.
        """
        RESIDUES = ["MET", "CYS", "PHE", "TYR", "TRP"]
        SULPHUR_RESIS = ["MET", "CYS"]
        AROMATIC_RESIS = ["PHE", "TYR", "TRP"]

        aromatic_sulphur_df = self.filter_dataframe(
            self.rgroup_df, "resi_name", RESIDUES, True
        )
        distmat = self.compute_distmat(aromatic_sulphur_df)
        interacting_atoms = self.get_interacting_atoms_(5.3, distmat)
        interacting_atoms = zip(interacting_atoms[0], interacting_atoms[1])

        for (a1, a2) in interacting_atoms:
            resi1 = aromatic_sulphur_df.loc[a1, "node_id"]
            resi2 = aromatic_sulphur_df.loc[a2, "node_id"]

            condition1 = resi1 in SULPHUR_RESIS and resi2 in AROMATIC_RESIS
            condition2 = resi1 in AROMATIC_RESIS and resi2 in SULPHUR_RESIS

            if (condition1 or condition2) and resi1 != resi2:
                if self.has_edge(resi1, resi2):
                    self.edges[resi1, resi2]["kind"].add("aromatic_sulphur")
                else:
                    self.add_edge(resi1, resi2, kind={"aromatic_sulphur"})

    def add_cation_pi_interactions_(self):
        cation_pi_df = self.filter_dataframe(
            self.rgroup_df, "resi_name", CATION_PI_RESIS, True
        )
        distmat = self.compute_distmat(cation_pi_df)
        interacting_atoms = self.get_interacting_atoms_(6, distmat)
        interacting_atoms = zip(interacting_atoms[0], interacting_atoms[1])

        for (a1, a2) in interacting_atoms:
            resi1 = cation_pi_df.loc[a1, "node_id"]
            resi2 = cation_pi_df.loc[a2, "node_id"]

            condition1 = resi1 in CATION_RESIS and resi2 in PI_RESIS
            condition2 = resi1 in PI_RESIS and resi2 in CATION_RESIS

            if (condition1 or condition2) and resi1 != resi2:
                if self.has_edge(resi1, resi2):
                    self.edges[resi1, resi2]["kind"].add("cation_pi")
                else:
                    self.add_edge(resi1, resi2, kind={"cation_pi"})

    def get_edges_by_bond_type(self, bond_type):
        """
        Parameters:
        ===========
        - bond_type: (str) one of the elements in the variable BOND_TYPES

        Returns:
        ========
        - resis: (list) a list of tuples, where each tuple is an edge.
        """

        resis = []
        for n1, n2, d in self.edges(data=True):
            if bond_type in d["kind"]:
                resis.append((n1, n2))
        return resis

    def compute_all_edge_features(self):
        """
        Calls on compute_edge_features (below).
        """
        for edge in self.edges():
            self.compute_edge_features(edge)

    def compute_edge_features(self, edge):
        """
        A function that computes one edge's features from the data.

        The features are:
        -----------------
        - one-of-K encoding for bond type [8 cells]
        """

        # Defensive programming checks start!
        assert len(edge) == 2, "Edge must be a 2-tuple."
        u, v = edge
        assert self.has_edge(u, v), "Edge not present in graph."
        # Defensive programming checks end.

        # Encode one-of-K for bond type.
        bond_set = self.edges[u, v]["kind"]
        bond_features = self.encode_bond_features(bond_set)
        self.edges[u, v]["features"] = np.concatenate((bond_features,))

    def compute_all_node_features(self):
        """
        Calls on compute_node_features (below).
        """

        for n in self.nodes():
            self.compute_node_features(n)

    def compute_node_features(self, node, debug=False):
        """
        A function that computes one node's features from the data.

        The features are:
        -----------------
        - one-of-K encoding for amino acid identity at that node [23 cells]

        - the molecular weight of the amino acid [1 cell]

        - the pKa of the amino acid [1 cell]

        - the node degree, i.e. the number of other nodes it is connected to
          [1 cell] (#nts: not sure if this is necessary.)

        - the sum of all euclidean distances on each edge connecting those
          nodes [1 cell]

        - the types of bond edges it is participating in [8 cells, with each
          cell representing one of the bond types]

        Parameters:
        ===========
        - node:     A node present in the Protein Interaction Network.
        """

        # A defensive programming assertion!
        assert self.has_node(node)

        # Declare a convenience variable for accessing the amino acid name
        aa = self.node[node]["resi_name"]

        # Encode the amino acid as a one-of-K encoding.
        aa_lb = LabelBinarizer()
        aa_lb.fit(RESI_NAMES)
        # following line is hack-ish; needed to do [0] in order to get
        # dimensions correct.
        aa_enc = aa_lb.transform([aa])[0]

        # Encode the isoelectric point and mol weights of the amino acid.
        # These values are scaled between 0 and 1.
        pka = [ISOELECTRIC_POINTS_STD[aa]][0][0]

        mw = [MOLECULAR_WEIGHTS_STD[aa]][0][0]

        # Encode the degree of the node.
        deg = [self.degree(node)]

        # Encode the sum of euclidean distances on each edge connecting the
        # to the node.
        # Note: this is approximate, and only factors in the C-alpha distances
        # between the nodes, not the actual interaction distances.
        """For the time being, ignored. 21 April 2016"""
        sum_eucl_dist = 0
        for n2 in self.neighbors(node):
            dist = euclidean(self.node_coords(node), self.node_coords(n2))
            sum_eucl_dist += dist
        sum_eucl_dist = [sum_eucl_dist]

        # Encode the bond types that it is involved in
        bond_set = set()
        for n2 in self.neighbors(node):
            bond_set = bond_set.union(self.edges[node, n2]["kind"])
        bonds = self.encode_bond_features(bond_set)
        bonds = [i for i in bonds]
        # Code block ends for encoding bond types.

        # Finally, make the feature vector.
        # The single-value variables are enclosed in a list (above) to enable
        # concatenation in a numpy array.
        if debug:
            print("pka: {0}".format(pka))
            print("aa_enc: {0}".format(aa_enc))
            print("mw: {0}".format(mw))
            print("sum_eucl_dist: {0}".format(sum_eucl_dist))
            print("bonds: {0}".format(bonds))

        features = np.concatenate((aa_enc, pka, mw, deg, sum_eucl_dist, bonds))
        features = features.reshape(1, features.shape[0])
        self.node[node]["features"] = features

    def encode_bond_features(self, bond_set):
        """
        We break out this function for encoding bond types because it is
        reused and occupies several lines.

        Parameters:
        ===========
        - bond_set: (set or list) of bonds.
        """
        bond_lb = LabelBinarizer()
        bond_lb.fit(BOND_TYPES)

        bonds = np.zeros(len(BOND_TYPES))
        if len(bond_set) > 0:
            bond_array = bond_lb.transform([i for i in bond_set])

            for b in bond_array:
                bonds = bonds + b

        return bonds

    def node_coords(self, n):
        """
        A helper function for getting the x, y, z coordinates of a node.
        """
        x = self.node[n]["x"]
        y = self.node[n]["y"]
        z = self.node[n]["z"]

        return x, y, z

    def feature_array(self, kind):
        """
        A convenience function for getting all of the feature arrays from the
        nodes.

        Parameters:
        ===========
        - kind: (str) one of ['node', 'edge']

        Returns:
        ========
        if kind == 'node':
            return node features
        if kind == 'interactions':
            return edge features
        """
        assert kind in [
            "node",
            "edge",
        ], 'you must specify "node" or "edge"\
            for the "kind" parameter'

        if kind == "node":
            return np.array([d["features"] for n, d in self.nodes(data=True)])
        elif kind == "edge":
            return np.array(
                [d["features"] for u, v, d in self.edges(data=True)]
            )

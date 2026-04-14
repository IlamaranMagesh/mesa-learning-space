import pytest
import networkx as nx
from example.utilities import generate_random_subnetworks

class TestUtilities:
    @pytest.mark.parametrize("nodes, nodes_in_subnetwork", [(5, 2), (6, 0), (6, 4)])
    def test_generate_random_subnetworks_invalid_inputs(self, nodes, nodes_in_subnetwork):
        # Testing done:
        # Total Nodes cannot be odd
        # Subnetwork nodes cannot be odd
        # Total nodes should be equally subdivided to subnetworks
        with pytest.raises(ValueError):
            generate_random_subnetworks(nx.complete_graph(nodes), nodes_in_subnetwork)

    def test_generate_random_subnetworks_empty_graph(self):
        # Empty graph instance as input
        assert len(generate_random_subnetworks(nx.complete_graph(0),2)) == 0

    def test_generate_random_subnetworks(self):
        # Positive case
        subnetworks = generate_random_subnetworks(nx.complete_graph(6), 2)
        assert len(subnetworks) == 3 and len(subnetworks[0]) == 2
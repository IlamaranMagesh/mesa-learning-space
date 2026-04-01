import pytest
from example.agents import Player
from mesa.model import Model
from mesa.discrete_space import Network
import networkx as nx

from example.utilities import generate_random_subnetworks

class MockModel(Model):
    """Mock model with no custom step"""


def test_get_players_in_lobby():
    seed = 31
    N = 12
    m = MockModel()
    main_network = nx.complete_graph(N)
    main_layout = nx.random_layout(main_network)

    grid = Network(
        G=main_network,
        capacity=N,
        layout=main_layout,
    )

    player_agents = list(Player.create_agents(
        model=m,
        n=N,
        cell=list(grid.all_cells)
    ))

    # generated from the utility function
    subnetwork = [[0, 1, 3, 4], [2, 6, 5, 8], [7, 10, 9, 11]]

    # Agentset has agents created in order, so the first agent ID is 0
    agents_in_lobby = player_agents[0].get_players_in_lobby(subnetwork[0]).cells

    assert len(agents_in_lobby) == 3
    assert all(i in agents_in_lobby for i in [1, 3, 4])




def test_generate_random_subnetworks():
    # Total Nodes cannot be odd
    with pytest.raises(ValueError):
        generate_random_subnetworks(nx.complete_graph(5), 2)

    # subnetwork nodes cannot be odd
    with pytest.raises(ValueError):
        generate_random_subnetworks(nx.complete_graph(6), 0)

    # Total nodes should be equally subdivided to subnetworks
    with pytest.raises(ValueError):
        generate_random_subnetworks(nx.complete_graph(6), 4)

    # Positive case
    subnetworks = generate_random_subnetworks(nx.complete_graph(6), 2)
    assert len(subnetworks) == 3 and len(subnetworks[0]) == 2

    assert len(generate_random_subnetworks(nx.complete_graph(0),2)) == 0




def test_agents(self):
    self.assertEqual(True, False)  # add assertion here


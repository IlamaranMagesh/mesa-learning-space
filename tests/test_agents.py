import pytest
from example.agents import Player
from mesa.model import Model
from mesa.discrete_space import Network
import networkx as nx

from example.utilities import generate_random_subnetworks

@pytest.fixture
def mock_model():
    class MockModel(Model):
        """Mock model with no custom step"""
    return MockModel()

@pytest.fixture
def mock_player(mock_model):
    """ Factory fixture for Player"""
    def _mock_player():
        m = mock_model
        return Player(m)

    return _mock_player

@pytest.fixture
def player_agents_list(mock_model, N = 12):
    m = mock_model
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

    return player_agents


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

class TestPlayer:
    def test_get_players_in_lobby(self, player_agents_list):
        player_agents = player_agents_list

        # generated from the utilities.generate_random_subnetworks function
        subnetwork = [[0, 1, 3, 4], [2, 6, 5, 8], [7, 10, 9, 11]]

        # Agentset has agents created in order, so the first agent ID is 0
        agents_in_lobby = player_agents[0].get_players_in_lobby(subnetwork[0]).cells
        assert all(i in [c.coordinate for c in agents_in_lobby] for i in [1, 3, 4])

    def test_get_players_in_lobby_empty_input(self, player_agents_list):
        # Empty list as input
        player_agents = player_agents_list
        agents_in_lobby = player_agents[0].get_players_in_lobby([]).cells
        assert agents_in_lobby == []

    @pytest.mark.parametrize("toxic_spread, expected", [(100, 100), (0, 50), (150, 100)])
    def test_add_toxicity(self, mock_player, toxic_spread, expected):
        player = mock_player()
        player.add_toxicity(toxic_spread)
        assert player.mental_stress == expected

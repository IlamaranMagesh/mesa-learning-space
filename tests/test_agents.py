import pytest
from example.agents import Player
from mesa.model import Model
from mesa.discrete_space import Network
import networkx as nx

N = 12

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
def player_agents_list(mock_model, n = N):
    m = mock_model
    main_network = nx.complete_graph(n)
    main_layout = nx.random_layout(main_network)

    grid = Network(
        G=main_network,
        capacity=n,
        layout=main_layout,
    )

    player_agents = list(Player.create_agents(
        model=m,
        n=n,
        cell=list(grid.all_cells)
    ))

    return player_agents

class TestPlayer:
    def test_get_players_in_lobby(self, player_agents_list):
        player_agents = player_agents_list

        # lobbies generated from the utilities.generate_random_subnetworks function
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

    def test_player_post_step_convert_to_toxic(self, mock_player):
        player = mock_player()
        player.add_toxicity(100)
        player.post_step()

        assert player.mental_stress == 80
        assert player.is_toxic is True

    def test_toxic_player_post_step_ignore_toxicity(self, mock_player):
        player = mock_player()
        player.add_toxicity(100)
        player.post_step()

        # Toxic player should not accept toxicity
        player.add_toxicity(50)
        assert player.mental_stress == 80

    def test_toxic_player_post_step_remove_toxicity(self, mock_player):
        player = mock_player()
        player.add_toxicity(100)
        player.post_step()

        # Reducing toxicity to normal state
        player.post_step()
        player.post_step()

        assert player.is_toxic is False

    def test_toxic_player_step_spreading_toxicity(self, player_agents_list, subtests):
        player_agents = player_agents_list

        # lobbies generated from the utilities.generate_random_subnetworks function
        lobbies = [[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]]

        for i in range(5):
            player_agents[i].lobbyID = 0

        # Add toxicity and set 0th player as toxic
        player_agents[0].add_toxicity(100) # mental_stress = 100
        player_agents[0].post_step() # Note: Post-step reduces an amount of toxicity. Now, mental_stress = 80

        # Spread toxicity. toxic_spread = 1;
        player_agents[0].step(lobbies=lobbies)

        for i in range(1, 6):
            with subtests.test(msg="mental_stress of players in lobby after toxic_spread", i=i):
                assert player_agents[i].mental_stress == 50.5




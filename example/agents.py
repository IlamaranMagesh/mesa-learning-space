import mesa
from mesa.discrete_space import CellAgent, CellCollection, Cell

class Player(CellAgent):
    is_toxic = False
    _base_threshold = 50

    @property
    def base_threshold(self):
        return self._base_threshold

    @base_threshold.setter
    def base_threshold(self, value: int):
        if 0 <= value <= 100:
            self.base_threshold = value
        else:
            raise ValueError

    def __init__(
        self,
        model: mesa.Model,
        mental_stress: float = 50.0,
        recovery_rate: float = 0.2,
        tolerance: int = 50,
        cell: Cell | None = None
    ):
        """
        A Player agent assigned to a coordinate or ID

        :param model: Mesa model for the simulation
        :param mental_stress: Current mental state of the Player. Range: 0 (Healthy) to 100 (Toxic)
        :param recovery_rate: Percentage of mental_stress recovered after each game session. Range: 0 to 100
        :param tolerance: Tolerance level of the Player to toxic spread. Range: 0 to 100
        :param cell: Cell where the Player is placed. Cell coordinate is the Player ID
        """
        super().__init__(model)
        self.threshold: float = self.base_threshold + ((tolerance / 100) * (100 - self.base_threshold))
        self.tolerance: int = tolerance
        self.mental_stress = mental_stress
        self.recovery_rate = recovery_rate
        self.lobbyID: int | None = None
        self.cell = cell

        if self.mental_stress > self.threshold:
            self.is_toxic = True

    def get_players_in_lobby(self, current_lobby:list[int]) -> CellCollection:
        """
        To retrieve the Players in the same lobby as the current Player

        :param current_lobby: List of Player coordinates or IDs that are present in the lobby
        :return: CellCollection of the Player agents in the current_lobby
        """
        return self.cell.neighborhood.select(filter_func = lambda player:
                                                                True if player.coordinate in current_lobby
                                                                else False)

    def add_toxicity(self, toxic_spread: float):
        """
        This method adds a specific amount of incoming toxic to the Player's mental stress based on the tolerance

        :param toxic_spread: Incoming toxic from other toxic Players
        """
        if not self.is_toxic:
            # Toxic reduction is an inverse function of tolerance
            self.mental_stress = min(self.mental_stress + toxic_spread * (1 - (self.tolerance / 100)), 100)


    def post_step(self):
        """
        Post game where some amount of mental stress of the Players is recovered based on their recovery_rate
        """
        # Exponential mental_stress decay 100 (Toxic) --> 0 (Healthy)
        self.mental_stress = max(0.0, self.mental_stress - (self.mental_stress * self.recovery_rate))

        if self.mental_stress > self.threshold:
            self.is_toxic = True
        else:
            self.is_toxic = False


    def step(self, lobbies: list[list[int]] | None = None):
        """
        Represents a game session with a group of players in a shared lobby.
        Each game, if a Player is toxic, they spread some amount of toxic to other non-toxic Players in the same lobby

        :param lobbies: List of all lobbies with Player coordinates or IDs for the current game session
        """
        if self.is_toxic:
            # Spread toxic to other players in the lobbyID
            current_lobby = lobbies[self.lobbyID]
            players_in_lobby = self.get_players_in_lobby(current_lobby)

            toxic_spread = (self.mental_stress - self.threshold) * self.recovery_rate

            for player in players_in_lobby.agents:
                player.add_toxicity(toxic_spread)





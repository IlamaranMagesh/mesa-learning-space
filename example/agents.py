import mesa
from mesa.discrete_space import CellAgent

BASE_THRESHOLD = 50

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
    ):
        super().__init__(model)
        self.threshold: float = self.base_threshold + ((tolerance / 100) * (100 - self.base_threshold))
        self.mental_stress = mental_stress
        self.recovery_rate = recovery_rate
        self.lobby: int | None = None

        if self.mental_stress > self.threshold:
            self.is_toxic = True

    def pre_step(self) -> None:
        # Exponential mental_stress decay 100 (Toxic) --> 0 (Healthy)
        self.mental_stress = min(0.0, self.mental_stress - (self.mental_stress * self.recovery_rate))

    def step(self) -> None:
        if self.is_toxic:
            ...



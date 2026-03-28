Toxic spread across players in game lobbies

Goal: how many games does it take % players to reach toxic level?

Toxic Player -- Spreads % of Toxic --> Other Players in the lobby

Agents:\
Attributes:
- mental-state # Current menta-state. Above the agent threshold, the agent is toxic
- toxic-threshold # The threshold above which the agent becomes toxic. f(tolerance)
- recovery-rate # The rate at which the agent recovers from toxicity
- tolerance # The amount of toxicity that the agent can tolerate
- toxic-spread # The amount of toxicity that the agent spreads to other players
- is-toxic # Whether the agent is currently toxic

## Flow:

### Model steps:

Creates lobbies and updates the lobbyID of the agents before each step
(lobbyID can be updated by using AgentSet.to_list since the order is the same as creation, so the agent id is the
idx of the agent in the set)

Agents do pre-step

Agents do step with lobbies sent

### Agent steps:

pre-step: each agent updates their current mental-state based on recovery-rate, if reduced below change
state to not toxic

step: each agents check their lobby and infect players if infected. During toxic spread
all other agents get some amount of increase in mental-state based on their tolerance.




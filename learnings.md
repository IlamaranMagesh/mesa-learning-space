### Frictions

- It would be better to have a feature to filter neighbouring agents based on the
type of edges they are connected to in `network` space. (like in networkx)


- Inheriting CellAgent/FixedAgent doesn't provide cell attribute on using `create_agents()`.
This is because of the MRO of the classes. `class CellAgent(Agent, HasCell, BasicMovement)`, here
the `HasCell` has the `cell` attribute and since `CellAgent` doesn't have `__init__`, the control goes to
`Agent` which doesn't have `cell` attribute causing no attribute error, unless the subclasses define `cell`
attribute.
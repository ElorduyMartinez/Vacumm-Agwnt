from mesa.visualization import CanvasGrid, ModularServer
from Robot import VacuumModel, VacuumAgent, Dirt
from mesa.visualization.UserParam import NumberInput
from mesa.visualization.UserParam import Choice
from mesa.visualization.modules import ChartModule


GRID_WIDTH = 10
GRID_HEIGHT = 10


def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}
    if isinstance(agent, VacuumAgent):
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    elif isinstance(agent, Dirt):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    return portrayal


simulation_params = {
    "num_agents": NumberInput(
        "Specify the number of agents participating in the simulation", value=1
    ),
    "grid_width": GRID_WIDTH,
    "grid_height": GRID_HEIGHT,
    "dirt_density": NumberInput(
        "Set the density of dirt on the grid (as a percentage of total cells)",
        value=0.2,
    ),
    "agent_behavior_mode": Choice(
        "Choose the agent behavior algorithm for the simulation",
        "bfs",
        ["bfs", "random", "dijkstra"],
    ),
}


chart_currents = ChartModule(
    [
        {"Label": "Cleaning Efficiency", "Color": "#2563eb"},  # Blue
        {"Label": "Dirt Remaining", "Color": "#dc2626"},  # Red
    ],
    canvas_height=300,
    data_collector_name="datacollector_currents",
)


grid = CanvasGrid(agent_portrayal, GRID_WIDTH, GRID_HEIGHT, 500, 500)
server = ModularServer(
    VacuumModel, [grid, chart_currents], "Vacuum Model", simulation_params
)

server.port = 8521
server.launch()

from mesa.visualization import CanvasGrid, ModularServer
from Robot import VacuumModel, VacuumAgent, Dirt


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

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(
    VacuumModel,
    [grid],
    "Vacuum Model",
    {"N": 1, "width": 10, "height": 10} 
)

server.port = 8521  
server.launch()

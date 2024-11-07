import time
from Robot import Dirt, VacuumModel
from Robot import VacuumAgent

# Parameters
num_vacuums = 5
width = 10
height = 10
dirt_density = 0.5
max_run_time = 30  # Run the model for 30 seconds at max
agent_behavior_mode = "bfs"
steps_per_second = 10  # Set the desired frames (steps per second)

# Initialize the model
model = VacuumModel(
    num_vacuums, width, height, dirt_density, agent_behavior_mode
)

# Start time
start_time = time.time()


print(f"Running Simulation...")

# Run the model until the specified time has passed
while time.time() - start_time < max_run_time:
    if model.get_dirt_remaining() == 0:
        break

    print(f"Dirt left: {model.get_dirt_remaining()}", end="\r")
    model.step()
    time.sleep(
        1 / steps_per_second
    )  # Pause to achieve the desired frames per second

# Calculate the necessary time until all cells are clean (or the maximum time is reached)
time_taken = time.time() - start_time

# Calculate the percentage of clean cells after the simulation
total_cells = width * height
total_dirt = len(
    [agent for agent in model.schedule.agents if isinstance(agent, Dirt)]
)
clean_cells = total_cells - total_dirt
clean_percentage = (clean_cells / total_cells) * 100

# Calculate the total number of movements made by all agents
total_movements = sum(
    agent.movements
    for agent in model.schedule.agents
    if isinstance(agent, VacuumAgent)
)

# Print results
print("Vacuum Cleaning Results:")
print(f"Time taken: {time_taken:.2f} seconds")
print(f"Percentage of clean cells: {clean_percentage:.2f}%")
print(f"Total movements by all agents: {total_movements}")

for agent in model.schedule.agents:
    if isinstance(agent, VacuumAgent):
        print(
            f"Vacuum ID {agent.unique_id} cleaned {agent.cleaned_dirt} dirt pieces."
        )

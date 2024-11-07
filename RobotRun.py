import time
from Robot import VacuumModel
from Robot import VacuumAgent

# Parameters
num_vacuums = 5
width = 10
height = 10
dirt_density = 0.5
run_time = 30  # Run the model for 30 seconds

# Initialize the model
model = VacuumModel(num_vacuums, width, height, dirt_density)

# Start time
start_time = time.time()

# Run the model until the specified time has passed
while time.time() - start_time < run_time:
    model.step()

# Print results
print("Vacuum Cleaning Results after 30 seconds:")
for agent in model.schedule.agents:
    if isinstance(agent, VacuumAgent):
        print(f"Vacuum ID {agent.unique_id} cleaned {agent.cleaned_dirt} dirt pieces.")
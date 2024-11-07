import mesa
import numpy as np
from collections import deque
import heapq

import mesa
import numpy as np

class VacuumModel(mesa.Model):
    def __init__(self, N, width, height, dirt_density=0.2):
        super().__init__()
        self.num_vacuums = N
        self.grid = mesa.space.MultiGrid(width, height, torus=False) 
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True

        num_dirt_cells = int(width * height * dirt_density)
        occupied_positions = set()  
        while len(occupied_positions) < num_dirt_cells:
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            if (x, y) not in occupied_positions:
                dirt = Dirt(self.next_id(), (x, y), self)
                self.grid.place_agent(dirt, (x, y))
                occupied_positions.add((x, y))

        for i in range(self.num_vacuums):
            placed = False
            while not placed:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                if (x, y) not in occupied_positions:
                    vacuum = VacuumAgent(i, self)
                    self.schedule.add(vacuum)
                    self.grid.place_agent(vacuum, (x, y))
                    occupied_positions.add((x, y))
                    placed = True

    def step(self):
        self.schedule.step()


class VacuumAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cleaned_dirt = 0  
        self.behavior_mode = 'bfs'  # Options: 'random', 'bfs', 'dijkstra'

    def move(self):
        if self.behavior_mode == 'bfs':
            next_step = self.bfs_find_dirt()
        elif self.behavior_mode == 'dijkstra':
            next_step = self.dijkstra_find_dirt()
        else:
            next_step = None

        if next_step and next_step != self.pos:
            # Move only one step towards the target
            self.model.grid.move_agent(self, next_step)
        else:
            self.random_move()

    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        if possible_steps:
            new_position = self.random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)

    def bfs_find_dirt(self):
        queue = deque([(self.pos, [])])
        visited = set()
        visited.add(self.pos)

        while queue:
            current_pos, path = queue.popleft()
            for neighbor in self.model.grid.get_neighborhood(current_pos, moore=True, include_center=False):
                if neighbor not in visited:
                    visited.add(neighbor)
                    cell_contents = self.model.grid.get_cell_list_contents([neighbor])
                    if any(isinstance(agent, Dirt) for agent in cell_contents):
                        return path[0] if path else neighbor 
                    queue.append((neighbor, path + [neighbor]))
        return None

    def dijkstra_find_dirt(self):
        distances = {tuple(pos): float('inf') for _, pos in self.model.grid.coord_iter()}
        distances[self.pos] = 0
        priority_queue = [(0, self.pos, [])]
        visited = set()

        while priority_queue:
            current_dist, current_pos, path = heapq.heappop(priority_queue)
            if current_pos in visited:
                continue
            visited.add(current_pos)
            cell_contents = self.model.grid.get_cell_list_contents([current_pos])
            if any(isinstance(agent, Dirt) for agent in cell_contents):
                return path[0] if path else current_pos  

            for neighbor in self.model.grid.get_neighborhood(current_pos, moore=True, include_center=False):
                if neighbor not in visited:
                    new_dist = current_dist + 1
                    if new_dist < distances[tuple(neighbor)]:
                        distances[tuple(neighbor)] = new_dist
                        heapq.heappush(priority_queue, (new_dist, neighbor, path + [neighbor]))

        return None

    def clean(self):
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        dirt_to_clean = [obj for obj in cell_contents if isinstance(obj, Dirt)]
        if dirt_to_clean:
            for dirt in dirt_to_clean:
                self.model.grid.remove_agent(dirt)
            self.cleaned_dirt += len(dirt_to_clean)

    def step(self):
        self.move()
        self.clean()


class Dirt(mesa.Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
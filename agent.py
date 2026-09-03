# agent.py
# Lab 03
import random
from collections import deque
import heapq
import math     # lab 04
class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

# Lab 03 
# Step 1.2: Implementing BFS, DFS, and UCS
class SearchAgent:
    def __init__(self):
        self.plan = []
        # self.active_algo = 'BFS'  # BFS Search
        # self.active_algo = 'DFS'  # DFS Search
        # self.active_algo = 'UCS'  # UCS Search
        self.active_algo = 'AStar'  # A* Star - Lab 04

    def _neighbors(self, pos, walls, grid_size):
        w, h = grid_size
        x, y = pos
        moves = [('Up', (x, y + 1)), ('Down', (x, y - 1)),
                  ('Left', (x - 1, y)), ('Right', (x + 1, y))]
        result = []
        for action, (nx, ny) in moves:
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in walls:
                result.append((action, (nx, ny)))
        return result

    def bfs_search(self, start, goal, walls, grid_size):
        frontier = deque([(start, [])])
        reached = {start}
        while frontier:
            pos, path = frontier.popleft()
            if pos == goal:
                return path
            for action, npos in self._neighbors(pos, walls, grid_size):
                if npos not in reached:
                    reached.add(npos)
                    frontier.append((npos, path + [action]))
        return []

    def dfs_search(self, start, goal, walls, grid_size):
        frontier = [(start, [])]
        reached = {start}
        while frontier:
            pos, path = frontier.pop()
            if pos == goal:
                return path
            for action, npos in self._neighbors(pos, walls, grid_size):
                if npos not in reached:
                    reached.add(npos)
                    frontier.append((npos, path + [action]))
        return []

    def ucs_search(self, start, goal, walls, grid_size):
        frontier = [(0, start, [])]
        reached = {start: 0}
        while frontier:
            cost, pos, path = heapq.heappop(frontier)
            if pos == goal:
                return path
            for action, npos in self._neighbors(pos, walls, grid_size):
                new_cost = cost + 1
                if npos not in reached or new_cost < reached[npos]:
                    reached[npos] = new_cost
                    heapq.heappush(frontier, (new_cost, npos, path + [action]))
        return []

    # Step 1.3: Executing and Comparing Offline Plans
    def sense_and_act(self, percept):
        if not self.plan:
            start = tuple(percept['agent_pos'])
            food_list = percept['all_food']
            if not food_list:
                return 'Up'
            goal = min(food_list, key=lambda f: abs(f[0]-start[0]) + abs(f[1]-start[1]))
            walls = set(percept['walls'])
            grid_size = percept['grid_size']

            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(start, goal, walls, grid_size)
            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(start, goal, walls, grid_size)
            elif self.active_algo == 'AStar':   # Lab 04
                self.plan = self.astar_search(start, goal, walls, grid_size, heuristic_type='manhattan')
            else:
                self.plan = self.ucs_search(start, goal, walls, grid_size)

        return self.plan.pop(0) if self.plan else 'Up'

    # lab 04
    # Step 1.1: Implementing the Heuristic Functions
    def manhattan_distance(self, pos, goal):
        return abs(pos[0]-goal[0]) + abs(pos[1]-goal[1])

    def euclidean_distance(self, pos, goal):
        return math.sqrt((pos[0]-goal[0])**2 + (pos[1]-goal[1])**2)

    # Step 1.2: Implementing A* Search
    def astar_search(self, start_pos, goal_pos, walls, grid_size, heuristic_type='manhattan'):
        h_fn = self.manhattan_distance if heuristic_type == 'manhattan' else self.euclidean_distance

        frontier = []
        h0 = h_fn(start_pos, goal_pos)
        heapq.heappush(frontier, (h0, 0, start_pos, []))
        reached_states = set()

        while frontier:
            f_cost, g_cost, current_pos, path_taken = heapq.heappop(frontier)

            if current_pos == goal_pos:
                return path_taken

            if current_pos in reached_states:
                continue
            reached_states.add(current_pos)

            for action, npos in self._neighbors(current_pos, walls, grid_size):
                if npos not in reached_states:
                    g_new = g_cost + 1
                    h_new = h_fn(npos, goal_pos)
                    f_new = g_new + h_new
                    heapq.heappush(frontier, (f_new, g_new, npos, path_taken + [action]))

        return []
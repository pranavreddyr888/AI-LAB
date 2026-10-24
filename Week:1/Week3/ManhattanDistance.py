
import heapq

# Initial state (0 represents the blank tile)
initial_state = (2, 8, 3,
                 1, 6, 4,
                 7, 0, 5)

# Goal state
goal_state = (1, 2, 3,
              8, 0, 4,
              7, 6, 5)


# Calculate Manhattan Distance
def manhattan_distance(state, goal):
    distance = 0

    for i in range(9):
        tile = state[i]

        if tile != 0:
            current_row, current_col = divmod(i, 3)
            goal_index = goal.index(tile)
            goal_row, goal_col = divmod(goal_index, 3)

            distance += abs(current_row - goal_row)
            distance += abs(current_col - goal_col)

    return distance


# Generate neighboring states
def get_neighbors(state):
    neighbors = []
    blank = state.index(0)
    row, col = divmod(blank, 3)

    # Up, Down, Left, Right
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in moves:
        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_blank = new_row * 3 + new_col
            new_state = list(state)

            new_state[blank], new_state[new_blank] = (
                new_state[new_blank], new_state[blank]
            )

            neighbors.append(tuple(new_state))

    return neighbors


# A* Search Algorithm
def a_star(initial, goal):
    h = manhattan_distance(initial, goal)

    # Priority queue stores (f, g, state)
    pq = [(h, 0, initial)]

    parent = {initial: None}
    cost = {initial: 0}
    explored = 0

    while pq:
        f, g, current = heapq.heappop(pq)

        # Ignore outdated entries
        if g != cost[current]:
            continue

        explored += 1

        # Check whether goal is reached
        if current == goal:
            path = []

            while current is not None:
                path.append(current)
                current = parent[current]

            path.reverse()
            return path, explored

        # Explore neighboring states
        for neighbor in get_neighbors(current):
            new_g = g + 1

            if neighbor not in cost or new_g < cost[neighbor]:
                cost[neighbor] = new_g
                parent[neighbor] = current

                h = manhattan_distance(neighbor, goal)
                new_f = new_g + h

                heapq.heappush(
                    pq, (new_f, new_g, neighbor)
                )

    return None, explored


# Display a puzzle state
def display_state(state):
    for i in range(0, 9, 3):
        print(*[
            "_" if tile == 0 else tile
            for tile in state[i:i + 3]
        ])
    print()


# Main program
print("A* SEARCH USING MANHATTAN DISTANCE")
print("\nInitial State:")
display_state(initial_state)

print("Initial Manhattan Distance:",
      manhattan_distance(initial_state, goal_state))

path, explored = a_star(initial_state, goal_state)

if path:
    print("Solution Path:\n")

    for step, state in enumerate(path):
        print("Step:", step)
        display_state(state)

    print("Total Moves:", len(path) - 1)
    print("States Explored:", explored)

else:
    print("No solution found.")

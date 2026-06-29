import random
from math import inf


GRAPH = {
    "A": {"B": 17, "C": 5, "E": 8},
    "B": {"A": 17},
    "C": {"A": 5, "D": 17, "E": 17, "G": 45},
    "D": {"C": 17, "E": 9, "F": 11, "G": 22},
    "E": {"A": 8, "C": 17, "D": 9},
    "F": {"D": 11, "G": 13},
    "G": {"C": 45, "D": 22, "F": 13},
}

START = "A"
FINISH = "G"

ANTS_COUNT = 40
ITERATIONS = 60

ALPHA = 1
BETA = 3
RHO = 0.35
Q = 100
SEED = 11


def edge_key(vertex1, vertex2):
    return tuple(sorted((vertex1, vertex2)))


# длина пути
def path_length(path):
    total = 0

    for i in range(len(path) - 1):
        total += GRAPH[path[i]][path[i + 1]]

    return total


def path_to_string(path):
    return " -> ".join(path)


# расчет вероятностей выбора
def choose_next_vertex(current, visited, pheromone, rng):
    candidates = []
    probabilities = []

    for neighbor, distance in GRAPH[current].items():
        if neighbor not in visited:
            tau = pheromone[edge_key(current, neighbor)]
            eta = 1 / distance

            value = (tau ** ALPHA) * (eta ** BETA)

            candidates.append(neighbor)
            probabilities.append(value)

    if not candidates:
        return None

    total = sum(probabilities)
    random_value = rng.random() * total

    current_sum = 0

    for candidate, probability in zip(candidates, probabilities):
        current_sum += probability

        if current_sum >= random_value:
            return candidate

    return candidates[-1]


# построение пути муравья
def build_ant_path(pheromone, rng):
    current = START
    path = [current]
    visited = {current}

    while current != FINISH:
        next_vertex = choose_next_vertex(
            current=current,
            visited=visited,
            pheromone=pheromone,
            rng=rng
        )

        if next_vertex is None:
            return None

        path.append(next_vertex)
        visited.add(next_vertex)
        current = next_vertex

    return path


# алгоритм муравьиной колонии
def ant_colony_algorithm():
    rng = random.Random(SEED)

    # инициализация феромона
    pheromone = {}

    for vertex in GRAPH:
        for neighbor in GRAPH[vertex]:
            pheromone[edge_key(vertex, neighbor)] = 1.0

    best_path = None
    best_length = inf

    print("\nКРАТЧАЙШИЙ ПУТЬ В ГРАФЕ")
    print("Метод: алгоритм муравьиной колонии\n")

    for iteration in range(1, ITERATIONS + 1):
        successful_paths = []

        # запуск муравьев
        for ant in range(1, ANTS_COUNT + 1):
            path = build_ant_path(pheromone, rng)

            if path is not None:
                length = path_length(path)
                successful_paths.append((path, length))

                if length < best_length:
                    best_path = path.copy()
                    best_length = length

        # Испарение феромона
        for edge in pheromone:
            pheromone[edge] *= (1 - RHO)

        # Добавление феромона на успешные пути
        for path, length in successful_paths:
            delta_pheromone = Q / length

            for i in range(len(path) - 1):
                edge = edge_key(path[i], path[i + 1])
                pheromone[edge] += delta_pheromone

        # Лучший путь на текущей итерации
        if successful_paths:
            iteration_best_path, iteration_best_length = min(
                successful_paths,
                key=lambda item: item[1]
            )
        else:
            iteration_best_path = None
            iteration_best_length = None

        # Подробный вывод первых 10 итераций
        if iteration <= 10 or iteration % 10 == 0:
            print(f"Итерация {iteration}")
            print(f"Успешных муравьев: {len(successful_paths)} из {ANTS_COUNT}")

            if iteration_best_path is not None:
                print(
                    f"Лучший путь на итерации: "
                    f"{path_to_string(iteration_best_path)}, "
                    f"длина = {iteration_best_length}"
                )

            print(
                f"Лучший путь за все время: "
                f"{path_to_string(best_path)}, "
                f"длина = {best_length}"
            )

            print()

    print("ИТОГ:")
    print(f"Лучший найденный путь: {path_to_string(best_path)}")
    print(f"Длина пути: {best_length}")

    return best_path


def check_by_bruteforce():
    all_paths = []

    def dfs(current, path):
        if current == FINISH:
            all_paths.append(path.copy())
            return

        for neighbor in GRAPH[current]:
            if neighbor not in path:
                path.append(neighbor)
                dfs(neighbor, path)
                path.pop()

    dfs(START, [START])

    best_path = min(all_paths, key=path_length)

    print("\nПРОВЕРКА ПОЛНЫМ ПЕРЕБОРОМ:")
    print(f"Оптимальный путь: {path_to_string(best_path)}")
    print(f"Длина: {path_length(best_path)}")


if __name__ == "__main__":
    ant_colony_algorithm()
    check_by_bruteforce()
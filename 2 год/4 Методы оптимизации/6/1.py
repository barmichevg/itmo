import random
from itertools import permutations


DISTANCES = [
    [0, 1, 11, 10, 5],
    [1, 0, 11, 6, 10],
    [11, 11, 0, 6, 1],
    [10, 6, 6, 0, 1],
    [5, 10, 1, 1, 0],
]

CITY_NAMES = ["1", "2", "3", "4", "5"]

POPULATION_SIZE = 4
MUTATION_PROBABILITY = 0.01
GENERATIONS = 100
SEED = 1


# длина пути
def route_length(route):
    total = 0

    for i in range(len(route) - 1):
        total += DISTANCES[route[i]][route[i + 1]]

    return total


def route_to_string(route):
    return " -> ".join(CITY_NAMES[i] for i in route)


# приспособленность особи
def fitness(route):
    return 1 / route_length(route)


# созданпие начальной популяции
def create_initial_population(rng):
    population = []
    used_routes = set()

    while len(population) < POPULATION_SIZE:
        middle = [1, 2, 3, 4]
        rng.shuffle(middle)

        route = tuple([0] + middle + [0])

        if route not in used_routes:
            used_routes.add(route)
            population.append(list(route))

    return population


# выбор родителя для скрещивания
def roulette_selection(population, rng):
    fitness_values = [fitness(route) for route in population]
    total_fitness = sum(fitness_values)

    random_value = rng.random() * total_fitness
    current_sum = 0

    for route, fit in zip(population, fitness_values):
        current_sum += fit

        if current_sum >= random_value:
            return route.copy()

    return population[-1].copy()


# скрещивание
def order_crossover(parent1, parent2, rng):
    child = [None] * len(parent1)

    # Первый и последний город фиксированы
    child[0] = 0
    child[-1] = 0

    left, right = sorted(rng.sample(range(1, 5), 2))

    # Берем фрагмент от первого родителя
    child[left:right + 1] = parent1[left:right + 1]

    # Добавляем недостающие города из второго родителя
    remaining_genes = []

    for gene in parent2[1:-1]:
        if gene not in child:
            remaining_genes.append(gene)

    index = 1

    for gene in remaining_genes:
        while child[index] is not None:
            index += 1

        child[index] = gene

    return child


# мутация
def mutation(route, rng):
    if rng.random() < MUTATION_PROBABILITY:
        i, j = rng.sample(range(1, 5), 2)
        route[i], route[j] = route[j], route[i]

    return route


def print_population(title, population):
    print(title)
    print("-" * 80)
    print(f"{'№':<4} {'Маршрут':<35} {'Длина':<10} {'Fitness':<10}")
    print("-" * 80)

    for i, route in enumerate(population, start=1):
        print(
            f"{i:<4} "
            f"{route_to_string(route):<35} "
            f"{route_length(route):<10} "
            f"{fitness(route):<10.5f}"
        )

    print("-" * 80)
    print()


# основной цикл
def genetic_algorithm():
    rng = random.Random(SEED)

    population = create_initial_population(rng)
    best_route = min(population, key=route_length)

    print("\nЗАДАЧА КОММИВОЯЖЕРА")
    print("Метод: генетический алгоритм\n")

    print_population("Начальная популяция:", population)

    for generation in range(1, GENERATIONS + 1):
        children = []

        while len(children) < POPULATION_SIZE:
            parent1 = roulette_selection(population, rng)
            parent2 = roulette_selection(population, rng)

            child1 = order_crossover(parent1, parent2, rng)
            child2 = order_crossover(parent2, parent1, rng)

            child1 = mutation(child1, rng)
            child2 = mutation(child2, rng)

            children.append(child1)
            children.append(child2)

        children = children[:POPULATION_SIZE]
        extended_population = population + children

        extended_population.sort(key=route_length)
        population = extended_population[:POPULATION_SIZE]

        current_best = population[0]

        if route_length(current_best) < route_length(best_route):
            best_route = current_best.copy()

        if generation <= 3:
            print_population(f"Поколение {generation}:", population)

        if generation % 10 == 0:
            print(
                f"Поколение {generation}: "
                f"лучший маршрут = {route_to_string(best_route)}, "
                f"длина = {route_length(best_route)}"
            )

    print("\nИТОГ:")
    print(f"Лучший найденный маршрут: {route_to_string(best_route)}")
    print(f"Длина маршрута: {route_length(best_route)}")

    return best_route


def check_by_bruteforce():
    best_route = None
    best_length = float("inf")

    for middle in permutations([1, 2, 3, 4]):
        route = [0] + list(middle) + [0]
        length = route_length(route)

        if length < best_length:
            best_length = length
            best_route = route

    print("\nПРОВЕРКА ПОЛНЫМ ПЕРЕБОРОМ:")
    print(f"Оптимальный маршрут: {route_to_string(best_route)}")
    print(f"Длина: {best_length}")


if __name__ == "__main__":
    genetic_algorithm()
    check_by_bruteforce()
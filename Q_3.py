import random

class Individual:
    def __init__(self):
        self.board = [random.randint(0, 4) for _ in range(5)]
        self.fitness = self.calc_fitness()

    def calc_fitness(self):
        conflicts = 0
        for i in range(5):
            for j in range(i + 1, 5):
                if self.board[i] == self.board[j] or abs(self.board[i] - self.board[j]) == abs(i - j):
                    conflicts += 1
        return 10 - conflicts

    def create_combined_board(self, parent1, parent2):
        combined = Individual()
        combine_point = random.randint(0, 4)

        for i in range(combine_point):
            combined.board[i] = parent1.board[i]
        
        for i in range(combine_point, 5):
            combined.board[i] = parent2.board[i]
        
        combined.fitness = combined.calc_fitness()
        return combined


def genetic_algorithm():
    population = [Individual() for _ in range(100)]
    max_generations = 1000
    current_generation = 0

    while current_generation < max_generations:
        population.sort(key=lambda x: x.fitness, reverse=True)

        if population[0].fitness == 10:
            print(f"Solution found in {current_generation} generations")
            print(" ".join(map(str, population[0].board)))
            break

        new_population = []
        for _ in range(100):
            parent1, parent2 = random.sample(population, 2)
            combined = parent1.create_combined_board(parent1, parent2)

            if random.randint(0, 99) < 15:
                pos = random.randint(0, 4)
                combined.board[pos] = random.randint(0, 4)
                combined.fitness = combined.calc_fitness()

            new_population.append(combined)

        population = new_population
        current_generation += 1


genetic_algorithm()

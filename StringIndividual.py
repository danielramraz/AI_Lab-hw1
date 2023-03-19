from Individual import Individual


class StringIndividual(Individual):

    def __init__(self, gen: str):

        self.gen = gen
        self.gen_len = len(self.gen)
        self.age = 0
        self.score = 0

    def original_fitness(self):
        target = list("Hello, world!")
        score = 0
        for i in range(individual.gen_len):
            if individual.gen[i] == target[i]:
                score += 1

        bullsEyeScore = self.bulls_eye(individual, target, score)
        score = data.age_factor*individual.age + (1 - data.age_factor)*score
        bullsEyeScore = data.age_factor*individual.age + (1 - data.age_factor)*bullsEyeScore

        individual.score = (score, bullsEyeScore)

        return score, bullsEyeScore

    def bulls_eye_fitness(self, individual: Individual, target, score):  # exploitation
        for i in range(individual.gen_len):
            if individual.gen[i] == target[i]:
                score += 10
            elif individual.gen[i] in target:
                score += 5
        return score

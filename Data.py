from ParentOperator import ParentOperator


class Data:
    def __init__(self, pop_size: int, num_genes: int, max_generations: int, cross_operator: int, parent_selection: int, age_factor: float, max_age: int):
        self.pop_size = pop_size
        self.num_genes = num_genes
        self.max_generations = max_generations
        self.cross_operator = cross_operator
        self.parent_selection = parent_selection
        self.age_factor = age_factor
        self.max_age = max_age

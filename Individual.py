



class Individual:

    gen: str
    score: tuple
    gen_len: int

    def __init__(self, gen: str):
        self.gen = gen
        self.gen_len = len(self.gen)

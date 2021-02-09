import random


class TestModel:
    def __init__(self):
        self.a = [i for i in range(100000000)]
        pass

    def predict(self, inputs):
        return [random.random() for x in inputs]

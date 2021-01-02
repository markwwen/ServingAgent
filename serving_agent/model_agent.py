import time
import pickle

import redis


class ModelAgent:
    def __init__(
        self, redis_broker='localhost:6367', ModelClass, ModelConfig={}, 

    ):
        self.listen
        self.model = ModelClass(**ModelConfig)
        pass

    def run():
        while True:
            pass

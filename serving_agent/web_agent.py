import uuid
import time
import pickle
from typing import List

import redis


class WebAgent:
    def __init__(self, redis_broker='localhost:6379', redis_queue='broker', web_sleep=0.1, max_tries=6000, unpickling=True):
        parse = lambda x: {'host': x.split(':')[0], 'port': int(x.split(':')[1])}
        self.db = redis.StrictRedis(**parse(redis_broker))
        self.redis_queue = redis_queue
        self.web_sleep = web_sleep
        self.max_tries = max_tries
        self.unpickling = unpickling

    def process(self, batch: List) -> List:
        """
        input a batch, send items to redis broker and polling
        """
        keys = [str(uuid.uuid4()) for _ in range(len(batch))]
        with self.db.pipeline() as pipe:
            for key, model_input in zip(keys, batch):
                message = {'key': key, 'model_input': model_input}
                pipe.rpush(self.redis_queue, pickle.dumps(message))
            pipe.execute()

        # polling the redis broker
        num_tries = 0
        while num_tries < self.max_tries:
            time.sleep(self.web_sleep)
            num_tries += 1
            outputs = self.db.mget(keys)
            if None not in outputs:
                self.db.delete(*keys)
                if self.unpickling:
                    outputs = [pickle.loads(x) for x in outputs]
                return outputs
        else:
            return None


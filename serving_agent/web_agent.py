import uuid
import time
import pickle

import redis


class WebAgent:
    def __init__(self, redis_broker='localhost:6379', redis_queue='broker', web_sleep=0.1, max_tries=6000):
        parse = lambda x: {'host': x.split(':')[0], 'port': int(x.split(':')[1])}
        self.db = redis.StrictRedis(**parse(redis_broker))
        self.redis_queue = redis_queue
        self.web_sleep = web_sleep
        self.max_tries = max_tries

    def process(self, model_input):
        key = str(uuid.uuid4())
        message = {'key': key, 'model_input': model_input}
        self.db.rpush(self.redis_queue, pickle.dumps(message))
        num_tries = 0
        # polling the redis broker
        while num_tries < self.max_tries:
            time.sleep(self.web_sleep)
            num_tries += 1
            result = self.db.get(key)
            if result:
                model_output = pickle.loads(result)
                self.db.delete(key)
                return model_output
        else:
            return None


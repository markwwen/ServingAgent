import time
import pickle

import redis


class ModelAgent:
    def __init__(
        self,
        redis_broker='localhost:6379',
        redis_queue='broker',
        model_class=None,
        model_config={},
        batch_size=64,
        model_sleep=0.1,
        collection=False,
        collection_limit=6000,
    ):
        parse = lambda x: {'host': x.split(':')[0], 'port': int(x.split(':')[1])}
        self.db = redis.StrictRedis(**parse(redis_broker))
        self.redis_queue = redis_queue
        assert 'predict' in dir(model_class), 'No predict function in model class'
        self.model_class = model_class
        self.model_config = model_config
        self.batch_size = batch_size
        self.model_sleep = model_sleep
        self.collection = collection
        self.collection_limit = collection_limit

    def run(self, pre_process=lambda x: x, post_process=lambda x: x):
        model = self.model_class(**self.model_config)
        mq_miss = 0
        print('model init')
        while True:
            with self.db.pipeline() as pipe:
                pipe.lrange(self.redis_queue, 0, self.batch_size - 1)
                pipe.ltrim(self.redis_queue, self.batch_size, -1)
                queue, _ = pipe.execute()
            if queue:
                mq_miss = 0
                if not model:
                    model = self.model_class(**self.model_config)
                messages = [pickle.loads(x) for x in queue]
                keys = [message.get('key') for message in messages]
                model_inputs = [pre_process(message.get('model_input')) for message in messages]
                results = [post_process(x) for x in model.predict(model_inputs)]
                self.db.mset({key: pickle.dumps(result) for key, result in zip(keys, results)})
            else:
                mq_miss += 1
            print(mq_miss)
            if mq_miss and mq_miss % self.collection_limit == 0:
                mq_miss = 0
                if self.collection and model:
                    model = None
                    print('model is collected')

            time.sleep(self.model_sleep)

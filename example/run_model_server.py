from serving_agent import ModelAgent

from example.TestModel import TestModel

if __name__ == "__main__":
    model_agent = ModelAgent(redis_broker='localhost:6379', redis_queue='example', model_class=TestModel, collection=True, collection_limit=24000)
    model_agent.run()

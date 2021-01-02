<h1 align="center">Serving Agent</h1>

<p align="center">
一个用于模型服务化的轻量的中间件，其能提高 GPU 的利用率从而加速线上推理。
</p>

<h2 align="center">什么是 Serving Agent</h2>

Serving Agent 被设计为一个为模型服务化提供的的中间件，其可以被插入在 model server 和 web server 之间，通过帮助提升 GPU 利用率来提高线上推理性能。

对一个集成了机器学习模型的服务而言，通常从客户端而来的请求是流式的。为了发挥 GPU 并行计算的能力，我们通常引入一个消息队列来缓存从 web server 中接收到的请求再交由 model server 处理（其架构如下图所示）。Serving Agent 封装了一些如序列化/反序列化以及和消息队列通信（借助 reids 来实现）的细节操作。通过使用 Serving Agent，只要几行代码就可以构造起一个高性能的服务。

![model serving architecture](img/architecture.png)

<h2 align="center">安装</h2>

通过 `pip` 可以直接安装 ServingAgent，这需要 **Python >= 3.5**:

```bash
pip install serving_agent 
```

<h2 align="center">开发一个服务</h2>

1. 首先定义一个模型 [TestModel.py](./example/TestModel.py)。 模型中的 `predict` 函数需要接受一个批量的 input 作为参数。

```python
import random


class TestModel:
    def __init__(self):
        pass

    def predict(self, inputs):
        return [random.random() for x in inputs]
```

1. 开发一个 model server [run_model_server.py](./example/run_model_server.py) 并运行.

```python
from serving_agent import ModelAgent

from example.TestModel import TestModel

if __name__ == "__main__":
    model_agent = ModelAgent(redis_broker='localhost:6379', redis_queue='example', model_class=TestModel)
    model_agent.run()
```

```shell
python -m example.run_model_server
```

1. 使用 Flask 开发一个 web server （或任何别的 Python web 框架都可以） 并启动.

```python
from serving_agent import WebAgent
from flask import Flask, jsonify, request

app = Flask(__name__)
web_agent = WebAgent(redis_broker='localhost:6379', redis_queue='example')


@app.route('/api/test', methods=['POST'])
def test():
    parmas = request.get_json()
    data = parmas['data']
    result = web_agent.process(data)
    return jsonify({'data': result})


if __name__ == '__main__':
    app.run(debug=True)

```

```shell
python -m example.run_web_server
```

恭喜！你已经在几分钟内就开发了一个高性能的模型服务！
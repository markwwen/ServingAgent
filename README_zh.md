# Serving Agent

一个用于模型服务化的轻量的中间件，其能提高 GPU 的利用率从而加速推理。

## 什么是 Serving Agent

Serving Agent 被设计为一个为模型服务化提供的的中间件，其可以被插入在 model server 和 web server 之间，通过帮助提升 GPU 利用率来提高线上推理性能。

对一个继承了机器学习模型的服务而言，通常从客户端而来的请求是流式的。为了发挥 GPU 并行计算的能力，我们通常引入一个消息队列来缓存从 web server 中接收到的请求再交由 model server 处理（其架构如下图所示）。Serving Agent 封装了一些如序列化/反序列化以及和消息队列通信（借助 reids 来实现）的细节操作。通过使用 Serving Agent，只要几行代码就可以构造起一个高性能的服务。
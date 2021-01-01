# Serving Agent

A lightweight middleware for model serving to improving GPU utilization then speedup online inference. [中文 README](https://github.com/HughWen/ServingAgent/blob/main/README_zh.md)

## What is Serving Agent

Serving Agent is designed as a middleware for model serving between web server and model server to help the server improve the GPU utilization
then speedup online inference.
For the service with machile learning model, the requests from the client are usually streaming.
To utilize the parallel computing capability of GPUs, we usually import a message queue/message broker to cache the request from web server then batch process with model server (the below figure shows the architecture). Serving Agent encapsulates the detial actions that such as serialize the request data, communicate with message queue (redis) and deserialization and more over. With Serving Agent, it is easy to build a scalable service with serveral codes.
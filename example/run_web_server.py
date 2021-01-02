from flask import Flask, jsonify, request

from serving_agent import WebAgent

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

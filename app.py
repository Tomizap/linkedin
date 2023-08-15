from pprint import pprint

from flask import Flask, jsonify, request

from linkedin import LinkedIn

app = Flask(__name__)

@app.route('/multi_apply', methods=['POST'])
def multi_apply():
    print(request.json)
    bot = LinkedIn(request.json)
    bot.multi_apply()
    pprint(bot.data)
    return jsonify(bot.data)


if __name__ == '__main__':
    app.run(debug=True)

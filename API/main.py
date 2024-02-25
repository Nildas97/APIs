from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def test():
    """Addition of two numbers

    Returns:
        str: adds  two numbers
    """

    if (request.method == 'POST'):
        a = request.json["num1"]
        b = request.json["num2"]
        result = a + b
        return jsonify((str(result)))


@app.route('/abc', methods=['GET', 'POST'])
def test2():
    """Multiplication of two numbers

    Returns:
        str: two number product
    """
    if (request.method == 'POST'):
        a = request.json['num1']
        b = request.json['num2']
        result = a * b
        return jsonify((str(result)))


@app.route('/abc1', methods=['GET', 'POST'])
def test3():
    """Division of two numbers

    Returns:
        str: string 
    """
    if (request.method == 'POST'):
        a = request.json['num1']
        b = request.json['num2']
        result = a / b
        return jsonify((str(result)))


if __name__ == '__main__':
    app.run()

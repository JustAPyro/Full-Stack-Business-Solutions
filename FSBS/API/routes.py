from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return "hello"

@app.route('/name.json')
def names():
    return "['john', 'jane']"


if __name__ == '__main__':
    app.run()

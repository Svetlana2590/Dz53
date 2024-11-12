from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/2')
def hello_world2():  # put application's code here
    return 'Hello222 World!'


if __name__ == '__main__':
    app.run()

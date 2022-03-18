from flask import Flask

app = Flask(__name__)

print('working')

@app.route('/', methods=['GET','POST'])
def index():
    return "Hello Kirthivasan, How are you?"

if __name__ == "__main__":
    app.run()

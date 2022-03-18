from flask import Flask

app = Flask(__name__)

print('working')

@app.route('/', methods=['GET','POST'])
def index():
    return "Hello word"

if __name__ == "__main__":
    app.run()
# from app import app
from flask import Flask
from app.views import my_view

app = Flask(__name__)
app.register_blueprint(my_view)
if __name__ == '__main__':
    app.run(debug=False)

from flask import Flask
from flask_cors import CORS
from app.database import init_app
from app.views import *

app = Flask(__name__)

init_app(app)
CORS(app)

app.route('/', methods=['GET'])(index)
app.route('/api/users', methods=['POST'])(create_user)
app.route('/api/users', methods=['GET'])(get_all_users)
app.route('/api/users/<int:id>', methods=['GET'])(get_user)
app.route('/api/users/<int:id>', methods=['PUT'])(update_user)
app.route('/api/users/<int:id>', methods=['DELETE'])(delete_user)
app.route('/api/users/<string:email>', methods=['GET'])(get_user_by_email)


if __name__ == '__main__':
    app.run(debug=True)
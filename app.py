from datetime import timedelta

from flask import Flask, request, jsonify
from flask_jwt_simple import JWTManager, jwt_required, get_jwt_identity

from posts.post import Post
from tools.misc import make_resp, check_keys, create_jwt_generate_response
from posts.repo import InMemoryPostsRepo
from tools.my_json_encoder import MyJSONEncoder
from users.repo import InMemoryUsersRepo
from users.user import User

app = Flask(__name__)

app.json_encoder = MyJSONEncoder

app.user_repo = InMemoryUsersRepo()
app.post_repo = InMemoryPostsRepo()

app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRES'] = timedelta(hours=24)
app.config['JWT_IDENTITY_CLAIM'] = 'user'
app.config['JWT_HEADER_NAME'] = 'authorization'
app.jwt = JWTManager(app)

app.user_repo.request_create("who", "12345678")


@app.route("/", defaults={"path": ""})
@app.route("/u/<path:path>")
@app.route("/a/<path:path>")
def root(path):
    return app.send_static_file("index.html")


@app.route("/api/register", methods=['POST'])
def user_register():
    in_json = request.json

    if not in_json:
        return make_resp(jsonify({"message": "Empty request"}), 400)
    elif not check_keys(request.json, ('username', 'password')):
        return make_resp(jsonify({"message": "Bad request"}), 400)

    created_user = app.user_repo.request_create(**in_json)

    if created_user is None:
        return make_resp(jsonify({"message": "Duplicated user"}), 400)

    return create_jwt_generate_response(created_user)


@app.route("/api/login", methods=['POST'])
def user_login():
    in_json = request.json

    if not in_json:
        return make_resp(jsonify({"message": "Empty request"}), 400)
    elif not check_keys(request.json, ('username', 'password')):
        return make_resp(jsonify({"message": "Bad request"}), 400)

    user, error = app.user_repo.authorize(**in_json)

    if user is None:
        return make_resp(jsonify({"message": error}), 400)

    return create_jwt_generate_response(user)


@app.route('/api/posts/', methods=['GET'])
def get_all_posts():
    return make_resp(jsonify(app.post_repo.get_all()), 200)


@app.route('/api/posts', methods=['POST'])
@jwt_required
def add_post():
    in_json = request.json

    if not in_json:
        return make_resp(jsonify({"message": "Empty request"}), 400)
    elif not check_keys(request.json, ('category', 'type', 'title')):
        return make_resp(jsonify({"message": "Bad request"}), 400)

    post = Post(**in_json)
    post.author = User(**get_jwt_identity())
    post = app.post_repo.request_create(post)

    return make_resp(jsonify(post), 200)


@app.route('/api/post/<int:post_id>', methods=['GET'])
def get_post_by_id(post_id):
    return make_resp(jsonify(app.post_repo.get_by_id(post_id)), 200)


@app.route('/api/post/<int:post_id>', methods=['DELETE'])
@jwt_required
def delete_post_by_id(post_id):
    result = app.post_repo.request_delete(post_id, User(**get_jwt_identity()))
    if result:
        return make_resp(jsonify({'message': result}), 400)
    else:
        return make_resp(jsonify({'message': 'success'}), 200)


@app.route('/api/user/<username>', methods=['GET'])
def get_post_by_username(username):
    return make_resp(jsonify(app.post_repo.get_by_username(username)), 200)


@app.route('/api/posts/<category>', methods=['GET'])
def get_post_by_category(category):
    return make_resp(jsonify(app.post_repo.get_by_category(category)), 200)


if __name__ == '__main__':
    app.run()

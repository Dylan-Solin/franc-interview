from flask import Flask, render_template, jsonify, Response, request
import json, operator

app = Flask(__name__)

@app.route('/')
def index_view():
    username = request.args.get('username')
    posts = []
    if username:
        posts = prepare_user_posts(username)
    return render_template('index.html', username = username, posts = posts)

@app.route('/users')
def users_view():
    with open('./users.json', 'r') as f:
        users = f.read()
    return Response(users, mimetype="application/json")

@app.route('/posts')
def posts_view():
    with open('./posts.json', 'r') as f:
        posts = f.read()
    return Response(posts, mimetype="application/json")


def prepare_user_posts(username):
    with open('./posts.json', 'r') as f:
        posts = f.read()
    json_posts = json.loads(posts)
    
    with open('./users.json', 'r') as f:
        following = f.read()

    json_following = json.loads(following)
    json_following[username].append(username)

    user_posts = dict(filter(lambda x: x[0] in json_following[username],json_posts.items()))

    posts = []

    for key in user_posts.keys():
        for post in user_posts[key]:
            post["user"] = key
        posts = user_posts[key] + posts

    for key in user_posts.keys():
        posts=sorted(posts, key=operator.itemgetter('time'),reverse = True)

    return(posts)

if __name__ == '__main__':
    app.run(host='127.0.0.1')
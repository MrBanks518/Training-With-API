from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///brooklyn.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String(50))
    age = db.Column(db.String(2))
    name = db.Column(db.String(30))

    def __repr__(self):
        return '<Post %s>' % self.food

class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "food", "age", "name")
        model = Post

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

class PostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        return posts_schema.dump(posts)

    def post(self):
        new_post = Post(
            food=request.json['food'],
            age=request.json['age'],
            name=request.json['name']
        )
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)

class PostResource(Resource):

    def patch(self, post_id):
        post = Post.query.get_or_404(post_id)

        if 'food' in request.json:
            post.food = request.json['food']
        if 'age' in request.json:
            post.age = request.json['age']
        if 'name' in request.json:
            post.name = request.json['name']

        db.session.commit()
        return post_schema.dump(post)

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204

    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post_schema.dump(post)

api.add_resource(PostResource, '/posts/<int:post_id>')
api.add_resource(PostListResource, '/posts')

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')
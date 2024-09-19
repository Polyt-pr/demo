from flask import Flask, jsonify
import asyncio
from tortoise import Tortoise
from tortoise import Model
from tortoise.fields import CharField, IntField

app = Flask(__name__)

async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['__main__']}
    )
    await Tortoise.generate_schemas()

class User(Model):
    id = IntField(pk=True)
    name = CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        table = "user"

@app.route('/')
def hello():
    return jsonify({'hello': 'world'})

@app.route('/users')
async def users():
    users = await User.all()
    return jsonify([user.__dict__ for user in users])

@app.route('/users/<int:id>')
async def user(id):
    user = await User.get(id=id)
    return jsonify(user.__dict__)

@app.route('/users', methods=['POST'])
async def create_user():
    user = await User.create(name='John Doe')
    return jsonify(user.__dict__)

if __name__ == '__main__':
    asyncio.run(init())
    app.run()
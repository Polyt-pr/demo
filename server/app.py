from uuid import UUID
from server_types import db_types
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_uuid import FlaskUUID
import asyncio
from tortoise import Tortoise
from models import User, Poll, Response
from middleware import internal
from functools import wraps

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
FlaskUUID(app)

# initialize db
async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['__main__']}
    )
    await Tortoise.generate_schemas()

def async_route(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

# --------------------------------- GENERAL ---------------------------------- #

# validate api key
@app.route('/validate')
@internal()
@async_route
async def validate():
    return jsonify({'success': True})

# ----------------------------------- USER ----------------------------------- #

# get all users
@app.route('/users')
@internal()
@async_route
async def get_users():
    users = await User.all()
    return jsonify([user.__dict__ for user in users])

# create a new user (requires API key)
@app.route('/user', methods=['POST'])
@internal()
@async_route
async def create_user():
    if request.method == 'POST':
        user = await User.create()
        return jsonify(user.__dict__)
    
    return jsonify({'error': 'Invalid request'})

# delete user and all associated polls and responses (requires API key)
@app.route('/user/<uuid:user_id>', methods=['DELETE'])
@internal()
@async_route
async def delete_user(user_id):
    if request.method == 'DELETE':
        user = await User.get_or_none(id=user_id)

        if not user:
            return jsonify({'error': 'User not found'})

        await user.delete()
        return jsonify({'success': True})
    
    return jsonify({'error': 'Invalid request'})

# get user polls by id (requires valid user id)
@app.route('/user/<uuid:user_id>/polls')
@async_route
async def get_user_polls(user_id):
    if request.method == 'GET':
        user = await User.get_or_none(id=user_id)

        if not user:
            return jsonify({'error': 'User not found'})

        polls = await Poll.filter(user_id=user.id)  # Changed here
        return jsonify([poll.__dict__ for poll in polls])
    
    return jsonify({'error': 'Invalid request'})

# ----------------------------------- POLL ----------------------------------- #

# create a new poll (requires API key)
@app.route('/poll', methods=['POST'])
@internal()
@async_route
async def create_poll():
    if request.method == 'POST':
        data: db_types.CreatePollPayload = request.get_json()

        user = await User.get_or_none(id=data['user_id'])

        if not user:
            return jsonify({'error': 'User not found'})

        poll = await Poll.create(prompt=data['prompt'], user_id=user.id)  # Changed here

        response_ids: list[UUID] = []

        # create blank responses based on given number
        for _ in range(data['n_responses']):
            response = await Response.create(poll_id=poll.id)  # Changed here
            response_ids.append(response.id)

        res = poll.__dict__
        res['responses'] = response_ids

        return jsonify(res)
    
    return jsonify({'error': 'Invalid request'})

# get, delete, or update poll by id
@app.route('/poll/<uuid:id>', methods=['GET', 'DELETE', 'PATCH'])
@internal(methods=['DELETE', 'PATCH']) # only check API key for delete and patch
@async_route
async def get_poll(id):
    if request.method == 'GET':
        try: 
            poll = await Poll.get(id=id)
            return jsonify(poll.__dict__)
        except:
            return jsonify({'error': 'Poll not found'})

    if request.method == 'DELETE':
        poll = await Poll.get(id=id)
        await poll.delete()
        return jsonify({'success': True})

    # update (flip) poll status
    if request.method == 'PATCH':
        poll = await Poll.get(id=id)
        poll.active = not poll.active
        await poll.save()
        return jsonify(poll.__dict__)
    
    return jsonify({'error': 'Invalid request'})

@app.route('/poll/<uuid:id>/responses')
@async_route
async def get_poll_responses(id):
    if request.method == 'GET':
        poll = await Poll.get(id=id)
        responses = await Response.filter(poll_id=poll.id)
        return jsonify([response.__dict__ for response in responses])
    
    return jsonify({'error': 'Invalid request'})

# get all polls
@app.route('/polls')
@internal()
@async_route
async def get_polls():
    polls = await Poll.all()
    return jsonify([poll.__dict__ for poll in polls])

# --------------------------------- RESPONSE --------------------------------- #

@app.route('/response/<uuid:id>')
@async_route
async def get_response(id):
    if request.method == 'GET':
        response = await Response.get(id=id)
        return jsonify(response.__dict__)
    
    return jsonify({'error': 'Invalid request'})

# respond to a poll
@app.route('/response/<uuid:id>/respond', methods=['POST'])
@internal()
@async_route
async def respond_to_poll(id):
    if request.method == 'POST':
        data: db_types.RespondToPollPayload = request.get_json()
        response = await Response.get(id=id)
        response.text = data['text']
        await response.save()

        return jsonify(response.__dict__)
    
    return jsonify({'error': 'Invalid request'})

if __name__ == '__main__':
    asyncio.run(init())
    app.run()
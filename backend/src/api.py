import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from sqlalchemy.exc import SQLAlchemyError
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
Initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()


'''
    GET /drinks
    public endpoint
    contains only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks or
    appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def get_drinks():
    formatted_drinks = []

    try:
        for drink in Drink.query.all():
            formatted_drinks.append(drink.short())

        return jsonify({
            'success': True,
            'drinks': formatted_drinks
        })
    except SQLAlchemyError:
        abort(500)


'''
    GET /drinks-detail
    @TODO: it should require the 'get:drinks-detail' permission
    contains the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
    or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    formatted_drinks = []

    try:
        for drink in Drink.query.all():
            formatted_drinks.append(drink.long())

        return jsonify({
            'success': True,
            'drinks': formatted_drinks
        })
    except SQLAlchemyError:
        abort(500)


'''
    POST /drinks
    creates a new row in the drinks table
    responds with a 400 error if drink already exists
    @TODO: it should require the 'post:drinks' permission
    contains the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing
    only the newly created drink or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
def create_drink():
    try:
        json_content = request.get_json()
        # TODO: Validate title
        title = json_content['title']
        # TODO: Validate recipe
        recipe = json_content['recipe']

        existing_drink = Drink.query.filter_by(title=title).one_or_none()
        if not (existing_drink is None):
            abort(400)

        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except SQLAlchemyError:
        abort(500)


'''
    PATCH /drinks/<id>
    <id> is the existing model id
    responds with a 404 error if <id> is not found or drink is not found
    updates the corresponding row for <id>
    @TODO: it should require the 'patch:drinks' permission
    contains the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing
    only the updated drink or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
def update_drink(drink_id):
    try:
        # check if drink_id exists
        if drink_id is None:
            abort(404)

        drink = Drink.query.get(drink_id)

        # check if drink exists
        if drink is None:
            abort(404)

        json_content = request.get_json()
        # TODO: Validate title
        title = json_content['title']
        # TODO: Validate recipe
        recipe = json_content['recipe']

        drink.title = title
        drink.recipe = json.dumps(recipe)
        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })

    except SQLAlchemyError:
        abort(500)


'''
    DELETE /drinks/<id>
    <id> is the existing model id
    responds with a 404 error if <id> is not found or drink is not found
    it should delete the corresponding row for <id>
    @TODO it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
    or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
def delete_drink(drink_id):
    try:
        # check if drink_id exists
        if drink_id is None:
            abort(404)

        drink = Drink.query.get(drink_id)

        # check if drink exists
        if drink is None:
            abort(404)

        drink.delete()

        return jsonify({
            'success': False,
            'delete': drink_id
        })
    except SQLAlchemyError:
        abort(500)


''' Error handlers '''


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'Forbidden'
    }), 403


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not found'
    }), 404


@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable entity'
    }), 422


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal server error'
    }), 500

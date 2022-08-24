# https://geekflare.com/securing-flask-api-with-jwt/
# https://flask-jwt-extended.readthedocs.io/en/latest/basic_usage/
# https://www.youtube.com/watch?v=J5bIPtEbS0Q
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps
from flask import jsonify, request
from app.config import Config
from app.models.esp_model import Esp
from app import api, db

# https://www.youtube.com/watch?v=xF30i_A6cRw
api.authorizations = {
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-access-tokens'
    }
}

def login(data):
    if not data:
        # check if data exist
        response_object = {
            'message': 'Missing JSON in request'
        }
        return response_object,400
    
    # check if usernmae and password exist
    username = data['username']
    password = data['password']
    if not username:
        response_object = {
            'message': 'Missing username parameter'
        }
        return response_object, 400
    if not password:
        response_object = {
            'message': 'Missing password parameter'
        }
        return response_object, 400
    
    # check database if that user exists
    current_user = User.query.filter_by(user_name=username).first()
    # if username != 'Saminu' or password != 'Salisu':
    if not current_user:
        response_object = {
            'message': 'Bad username or password'
        }
        return response_object, 401
    else:        
        # access_token = jwt.encode({'user': username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, Config.SECRET_KEY)
        access_token = jwt.encode({'user': username}, Config.SECRET_KEY)
        response_object = {
                # 'access_token': access_token
                'access_token': access_token.decode('UTF-8')
            }
        return response_object, 200

# token required function
def token_required(f):  
    @wraps(f)  
    def decorated(*args, **kwargs):
        token = None 
        if 'x-access-tokens' in request.headers:  
            token = request.headers['x-access-tokens']             
                        
        if not token:  
            return {'message': 'a valid token is missing'}, 401
        try:
            # check esp db if token is there
            # data = jwt.decode(token, Config.SECRET_KEY)
            user = Esp.query.filter_by(text_api_token=token).first()
            user.name_company
        except:
            return {'message': 'token is invalid'}, 401 
        return f(*args,  **kwargs) 
    return decorated
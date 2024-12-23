"""Module for the Flask app."""

import os

from flask import Flask, redirect, request
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from .api.auth_routes import auth_routes
from .api.channel_routes import channel_routes
from .api.message_routes import message_routes
from .api.reaction_routes import reaction_routes
from .api.server_routes import server_routes
from .api.user_routes import user_routes
from .config import Config
from .models import User, db
from .seeds import seed_commands

app = Flask(__name__, static_folder='../../frontend/dist', static_url_path='/')
csrf = CSRFProtect(app)

# Setup login manager
login = LoginManager(app)
login.login_view = 'auth.unauthorized'


@login.user_loader
def load_user(id):
	"""Loads a user by their ID."""
	return User.query.get(int(id))


# Tell flask about our seed commands
app.cli.add_command(seed_commands)

app.config.from_object(Config)

app.register_blueprint(user_routes, url_prefix='/api/users')
app.register_blueprint(auth_routes, url_prefix='/api/auth')
app.register_blueprint(server_routes, url_prefix='/api/servers')
app.register_blueprint(channel_routes, url_prefix='/api/channels')
app.register_blueprint(message_routes, url_prefix='/api/messages')
app.register_blueprint(reaction_routes, url_prefix='/api/reactions')

db.init_app(app)
Migrate(app, db)

# Application Security
CORS(app)


# Since we are deploying with Docker and Flask,
# we won't be using a buildpack when we deploy to Heroku.
# Therefore, we need to make sure that in production any
# request made over http is redirected to https.
# Well.........
@app.before_request
def https_redirect():
	"""Redirects HTTP requests to HTTPS."""
	if os.environ.get('FLASK_ENV') == 'production':
		if request.headers.get('X-Forwarded-Proto') == 'http':
			url = request.url.replace('http://', 'https://', 1)
			code = 301
			return redirect(url, code=code)
		return None
	return None


"""
Commented out because we are now setting the CSRF in a dedicated route
and managing it in the frontend
"""
# @app.after_request
# def inject_csrf_token(response):
# 	"""Injects the CSRF token into the response."""
# 	token = generate_csrf()
# 	response.set_cookie(
# 		'csrf_token',
# 		token,
# 		secure=os.environ.get('FLASK_ENV') == 'production',
# 		samesite='Strict' if os.environ.get('FLASK_ENV') == 'production' else None,
# 		httponly=True,
# 	)
# 	response.headers['X-CSRFToken'] = token
# 	return response


@app.route('/api/docs')
def api_help():
	"""Returns all API routes and their doc strings."""
	acceptable_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
	return {
		rule.rule: [
			[method for method in rule.methods if method in acceptable_methods],
			app.view_functions[rule.endpoint].__doc__,
		]
		for rule in app.url_map.iter_rules()
		if rule.endpoint != 'static'
	}


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
	"""Route for handling favicon and index.html requests.

	This route will direct to the public directory in our
	react builds in the production environment for favicon
	or index.html requests
	"""
	if path == 'favicon.ico':
		return app.send_from_directory('public', 'favicon.ico')
	return app.send_static_file('index.html')


@app.errorhandler(404)
def not_found(e):
	"""Route for handling 404 errors."""
	return app.send_static_file('index.html')

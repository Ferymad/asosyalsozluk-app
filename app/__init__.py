from flask import Flask
from .routes.entry_routes import entry_routes

def create_app():
    app = Flask(__name__)
    # ... other configurations ...
    
    app.register_blueprint(entry_routes)
    
    return app
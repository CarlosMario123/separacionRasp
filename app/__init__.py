from flask import Flask
from app.config import Config
from app.db import init_db, close_db
from app.queues import start_background_threads
from app.routes import bp
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    logging.basicConfig(level=logging.INFO)
    
    with app.app_context():
        init_db()
    
    app.register_blueprint(bp)
    
    app.teardown_appcontext(close_db)
    
    start_background_threads()
    
    return app

from flask import Flask
from .database.dbconexion import Config
from .models.models import db
from .routes.routes import main, login_manager

def create_app():
    app = Flask(__name__,template_folder='../frontend/templates' ,static_folder='../frontend/static')
    app.config.from_object(Config)
    
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    with app.app_context():
        db.create_all()

    app.register_blueprint(main)

    return app 



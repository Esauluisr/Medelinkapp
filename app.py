from flask import Flask
from backend.database.dbconexion import Config
from backend.models.models import db
from backend.routes.routes import main, login_manager

def create_app():
    app = Flask(__name__,template_folder='./frontend/templates' ,static_folder='./frontend/static')
    app.config.from_object(Config)
    
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'main.index'

    with app.app_context():
        db.create_all()

    app.register_blueprint(main)

    return app 

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)



from flask import Flask

from extensions import *
from models import *
import os


from auth import auths
from views import view
from route import emp

def Application():
    try:
        app = Flask(__name__)
        app.config.from_pyfile('config.py')
        db.init_app(app)
        migrate.init_app(app, db)

        # user_datastore.init_app(db, User, Role)
        security.init_app(app, user_datastore)

        # app.jinja_env.globals.update(jobtype=data.getjobtype)

        app.register_blueprint(auths)
        app.register_blueprint(view)
        app.register_blueprint(emp)

        return app
        
    except Exception as Ae:
        logger.exception(Ae)
    
if __name__ == '__main__':
    Application().run(debug=True)
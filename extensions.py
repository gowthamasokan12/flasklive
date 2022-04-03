from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging

db = SQLAlchemy()
migrate = Migrate()

security = Security()

logger=logging.getLogger()

logging.basicConfig(filename="newfile.log",format='%(asctime)s %(message)s',  filemode='w') 
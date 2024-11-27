import logging 
import os
from flask import Flask

from app.users.routes import blueprint as users_blueprint
from app.dashboard.routes import blueprint as dashboard_blueprint
from app.map.routes import blueprint as map_blueprint
from app.table.routes import blueprint as table_blueprint
from app.database.routes import blueprint as database_blueprint
from app.settings.routes import blueprint as settings_blueprint

from app.extensions import db, migrate, login_manager, bcrypt, cache, socketio
import app.exceptions as app_exception

logging.basicConfig(
    level=logging.INFO,
    filename="log.log",
    encoding="utf-8"
)

def register_blueprint(app):
    app.register_blueprint(blueprint=users_blueprint)
    app.register_blueprint(blueprint=dashboard_blueprint)
    app.register_blueprint(blueprint=map_blueprint)
    app.register_blueprint(blueprint=table_blueprint)
    app.register_blueprint(blueprint=database_blueprint)
    app.register_blueprint(blueprint=settings_blueprint)


def register_error_handlers(app):
	app.register_error_handler(401, app_exception.unauthorized)
	app.register_error_handler(404, app_exception.page_not_found)
	app.register_error_handler(500, app_exception.server_error)


app = Flask(
    import_name=__name__,
    static_folder='assets',
    template_folder='templates'
)

register_blueprint(app)
register_error_handlers(app)
app.config.from_object('config.DevConfig')

db.init_app(app)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

from app.users.models import User
from app.database.models import Bakery, Amarnameh, OwnershipStatus, SecondFuel, HouseholdRisk, BakersRisk, TypeFlour, TypeBread
migrate.init_app(app=app, db=db)
login_manager.init_app(app=app)
bcrypt.init_app(app=app)
cache.init_app(app=app)
socketio.init_app(app=app)

login_manager.login_view = 'users.login'
login_manager.login_message = 'لطفا ابتدا وارد حساب کاربری خود بشوید!'
login_manager.login_message_category = 'info'
from flask import Flask, Blueprint
from flask_migrate import Migrate
from flask_restx import Api

from LMS.db import db
from LMS.config import DBConfig
from LMS.api import restaurant_ns, restaurant_contact_ns, \
                    lead_ns, manager_account_ns, order_ns, interaction_ns

def create_app():
    blueprint = Blueprint('api', __name__)
    api = Api(blueprint)
    api.add_namespace(restaurant_ns, path='/restaurants')
    api.add_namespace(restaurant_contact_ns, path='/restaurant_contacts')
    api.add_namespace(lead_ns, path='/leads')
    api.add_namespace(manager_account_ns, path='/manager_accounts')
    api.add_namespace(order_ns, path='/orders')
    api.add_namespace(interaction_ns, path='/interactions')

    app = Flask(__name__)
    app.register_blueprint(blueprint)
    app.config.from_mapping(
        SECRET_KEY="test_secret"
    )
    
    app.config.from_object(DBConfig)

    # DB init
    db.init_app(app)
    from LMS.models import ManagerAccounts, Restaurants, RestaurantContacts, Leads, Interactions, Orders
    migrate = Migrate(app, db)

    return app

if __name__=='__main__':
    create_app()

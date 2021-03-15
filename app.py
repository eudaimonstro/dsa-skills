import os
import sqlite3

import pandas as pd
from flask import Flask, Blueprint, json, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, Resource
import sqlite3

from db import db

from resources.member import Member, MemberList, member_ns, members_ns, viewer

app = Flask(__name__)
api_v1 = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_v1, version='1.0', title='DSA Skills',
          description='DSA Skills Test API')

app.register_blueprint(api_v1)
app.register_blueprint(viewer)

app.config.from_object('config.DevelopmentConfig')

api.add_namespace(member_ns)
api.add_namespace(members_ns)


@app.before_first_request
def create_tables():
    if not os.path.exists('development_database.db'):
        db.drop_all()
        db.create_all()
        initialize_sqlite_db(db)


def initialize_sqlite_db(db):
    with open(app.config['MEMBER_FILE_NAME'], 'r') as file:
        data_df = pd.read_csv(file)
        data_df.to_sql('members', con=db.get_engine(), index=False,
                       if_exists='append'
                       )


if __name__ == 'app':
    db.init_app(app)
    app.run()
    app.config['SERVER_NAME'] = 'localhost:5000'

from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy

md = MetaData( naming_convention = {
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s'
} )
db = SQLAlchemy( metadata = md )


class Doctor( db.Model ):
    __tablename__ = 'doctors'

    id = db.Column( db.Integer, primary_key = True )
    name = db.Column( db.String )
    created_at = db.Column( db.DateTime, server_default = db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate = db.func.now() )
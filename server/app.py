from flask import Flask, make_response
from models import db, Doctor
from flask_migrate import Migrate

app = Flask( __name__ )
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate( app, db )
db.init_app( app )

@app.route( '/doctors' )
def doctors():
    doc_list = []
    for d in Doctor.query.all():
        doc_list.append( {
            'id': d.id,
            'name': d.name,
            'created_at': d.created_at,
            'updated_at': d.updated_at
        } )
    return make_response( doc_list )
    

if __name__ == '__main__':
    app.run( port = 5555, debug = True )
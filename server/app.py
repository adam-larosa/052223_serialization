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
    # a list comprehension which is the same as the following for loop
    # doc_list = [ d.to_dict() for d in Doctor.query.all() ]
    doc_list = []
    for d in Doctor.query.all():
        doc_list.append( d.to_dict() )

    return make_response( doc_list )
    

if __name__ == '__main__':
    app.run( port = 5555, debug = True )
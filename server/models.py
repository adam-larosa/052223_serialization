from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

md = MetaData( naming_convention = {
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s'
} )
db = SQLAlchemy( metadata = md )


class Doctor( db.Model, SerializerMixin ):
    __tablename__ = 'doctors'

    serialize_rules = ( 
        # first we're taking out stuff from the Doctor model, created & updated
        '-created_at', '-updated_at', 
        
        # next we remove the nested relationships from the Appointment, we
        # want the appointments, but not the related doctor from the
        # appointment
        '-appointments.doctor',
        '-appointments.patient', 
        
        # the we bring in the patients
        'patients', 
        # but the patients have relationships that can lead back to this
        # doctor
        '-patients.appointments' 
    )

    id = db.Column( db.Integer, primary_key = True )
    name = db.Column( db.String )
    created_at = db.Column( db.DateTime, server_default = db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate = db.func.now() )

    appointments = db.relationship( 'Appointment', back_populates = 'doctor' )
    patients = association_proxy( 'appointments', 'patient' )

class Appointment( db.Model, SerializerMixin ):
    __tablename__ = 'appointments'

    serialize_rules = ( '-doctor_id', )
    id = db.Column( db.Integer, primary_key = True )
    note = db.Column( db.String )
    doctor_id = db.Column( db.Integer, db.ForeignKey( 'doctors.id' ) )
    patient_id = db.Column( db.Integer, db.ForeignKey( 'patients.id' ) ) 
    doctor = db.relationship( 'Doctor', back_populates = 'appointments' )
    patient = db.relationship( 'Patient', back_populates = 'appointments' )


class Patient( db.Model, SerializerMixin ):
    __tablename__ = 'patients'

    id = db.Column( db.Integer, primary_key = True )
    name = db.Column( db.String )

    appointments = db.relationship( 'Appointment', back_populates = 'patient' )

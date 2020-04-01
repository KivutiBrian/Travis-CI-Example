from main import db,ma
from sqlalchemy import func
from werkzeug.security import check_password_hash

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    full_name = db.Column(db.String(),nullable=False)
    email = db.Column(db.String(),nullable=False, unique=True)
    password = db.Column(db.String(),nullable=False)
    tasks = db.relationship('TaskModel',backref='user', lazy=True)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    def create_record(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    @classmethod
    def check_email_exists(cls,email):
        record = cls.query.filter_by(email=email).first()
        if record:
            return True
        else:
            return False

    @classmethod
    def validate_password(cls,email,password):
        record = cls.query.filter_by(email=email).first()
        if record and check_password_hash(record.password,password):
            return True
        else:
            return False

    @classmethod
    def get_userId(cls,email):
        return cls.query.filter_by(email=email).first().id

    @classmethod
    def get_userby_Id(cls,id):
        return cls.query.filter_by(id=id).first()

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id","full_name","email","create_at")
    
user_schema = UserSchema()
users_schema = UserSchema(many=True)
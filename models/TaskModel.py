from main import db,ma,app
from sqlalchemy import func

class TaskModel(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False) 
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())


    def create_record(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def fetch_all(cls):
        return cls.query.all()


    @classmethod
    def edit_task_byId(cls,id,title=None,description=None):
        record = cls.query.filter_by(id=id).first()
        if record:
            if title:
                record.title = title
            if description:
                record.description = description
            db.session.commit()
        return cls.query.filter_by(id=id).first()

    def delete_record(self):
        db.session.delete(self)
        db.session.commit()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ("id","title", "description","user_id","created_at")

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)




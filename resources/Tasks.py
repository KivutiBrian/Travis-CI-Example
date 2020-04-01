from main import Resource,api, fields,TaskModel,jwt_required,get_jwt_identity
from models.TaskModel import task_schema,tasks_schema
from models.UserModel import UserModel

# define my namespaces
ns_tasks = api.namespace('tasks', description="All operations regarding tasks")

# models
a_task_model = api.model('Task',{
    'title':fields.String(description="The task title",required=True),
    'description':fields.String(description="A short description about the task", required=True)
})


@ns_tasks.route('')
class TasksList(Resource):

    @api.doc(security='apikey')
    @jwt_required
    @api.response(200, 'Success')
    def get(self):
        """Get all the tasks"""
        user_id = get_jwt_identity()
        user = UserModel.get_userby_Id(user_id)
        user_tasks = user.tasks
        return tasks_schema.dump(user_tasks), 200

    @api.doc(security='apikey')
    @api.expect(a_task_model)
    @jwt_required
    def post(self):
        """Add a new task"""
        data = api.payload
        task = TaskModel(title=data['title'],description=data['description'],
                    user_id=get_jwt_identity())
        record = task.create_record()
        return task_schema.dump(record), 201

@ns_tasks.route('/<int:id>')
class Task(Resource):
    
    @api.doc(security='apikey')
    @jwt_required
    def get(self,id):
        task = next(filter(lambda a_task: a_task.id == id,TaskModel.fetch_all()),None)
        if task is not None:
            return task_schema.dump(task), 200
        else:
            return {'message':'Task does not exists'}, 404
    
    @api.doc(security='apikey')
    @api.expect(a_task_model)
    @jwt_required
    def put(self, id):
        data = api.payload
        task = next(filter(lambda a_task: a_task.id == id,TaskModel.fetch_all()),None)
        if task is not None:
            return task_schema.dump(TaskModel.edit_task_byId(id=id,**data)),200
        else:
            return {"message":"Task does not exists"}, 404

    @api.doc(security='apikey')
    @jwt_required    
    def delete(self,id):
        task = next(filter(lambda a_task: a_task.id == id,TaskModel.fetch_all()),None)
        if task:
            task.delete_task_byId()
            return {"message":"Task successfully deleted"}, 200
        else:
            return {"message":"Task does not exist"}, 404



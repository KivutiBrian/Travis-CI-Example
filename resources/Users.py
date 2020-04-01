from main import Resource,api,fields
from models.UserModel import UserModel,user_schema,users_schema

ns_users = api.namespace('users', description="All operations regarding users")


@ns_users.route('')
class UsersList(Resource):
    def get(self):
        """Get all the users"""
        return users_schema.dump(UserModel.fetch_all()), 200


@ns_users.route('/<int:id>')
class User(Resource):

    def get(self,id):
        pass

    def put(self,id):
        pass

    def delete(self,id):
        pass



from flask import Flask, request
from flask_restful import Resource, Api

import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super'
api = Api(app)


class Work_With_Pickle:
    ''' Work with module pickle'''
    def __init__(self, todos=None):
        if todos is None:
            self.todos = {
                'shop': 'Makeshopping',
            }

    def work_with_pickle(self, options='Write', filename='dick.pkl'):
        '''
        Test options is Write or Gettet
        to use different pickle options.
        Write: Write dictionary in file
        Getter: Get data from pickle

        '''
        if options == 'Write':
            file = open(filename, 'wb')
            pickle.dump(self.todos, file)
            file.close()
        elif options == 'Getter':
            file = open(filename, 'rb')
            self.todos = pickle.load(file)
            file.close()
        else:
            raise ValueError("Not recofnize command!")

    def __call__(self):
        return self.todos


class GetPutPostDelete(Resource):

    def get(selt, todo_id):
        todoer = Work_With_Pickle()
        todoer.work_with_pickle(options='Getter')
        if todo_id not in todoer():
            return {'error': f'{todo_id} not found'}, 404
        else:
            return {todo_id: todoer()[todo_id]}, 200

    def post(self, todo_id):
        toder = Work_With_Pickle()
        toder.work_with_pickle(options='Getter')
        toder()[todo_id] = request.form['data']
        toder.work_with_pickle(options='Write')
        return {todo_id: toder()[todo_id]}, 201

    def put(self, todo_id):
        toder = Work_With_Pickle()
        toder.work_with_pickle(options='Getter')
        if todo_id not in toder():
            raise ValueError("Not found {}".format(todo_id))
            return 404
        else:
            toder()[todo_id] = request.form['data']
            toder.work_with_pickle(options='Write')
            return {todo_id: toder()[todo_id]}, 201

    def delete(self, todo_id):
        toder = Work_With_Pickle()
        toder.work_with_pickle(options='Getter')
        try:
            del toder()[todo_id]
            toder.work_with_pickle(options='Write')
            return "Task {} delete successfuly".format(todo_id), 204
        except KeyError as e:
            print(e)


class GetAll(Resource):

    def __init__(self):
        self.work = Work_With_Pickle()
        self.work.work_with_pickle(options='Getter')

    def get(self):
        return self.work.todos


api.add_resource(GetAll, '/')
api.add_resource(GetPutPostDelete, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(host='192.168.1.5', debug=True)

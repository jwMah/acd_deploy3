from celery import Celery

# amqp://[username]:[password]@localhost:5672/
BROKER_URL = 'amqp://guest:guest@rabbitmq:5672/'

def make_celery(app):
    cell =  Celery(app.import_name, broker=BROKER_URL, )
    TaskBase = cell.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    cell.Task = ContextTask
    return cell

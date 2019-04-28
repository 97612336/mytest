from celery import Celery

app = Celery('add_tasks', broker='redis://127.0.0.1:6379', backend='redis://127.0.0.1:6379')


@app.task
def add_large_num(x, y):
    all_sum = 0
    for i in range(x):
        all_sum = (all_sum + i) * y
    return all_sum

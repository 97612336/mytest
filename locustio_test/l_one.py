from locust import HttpLocust, TaskSet


def index(l):
    l.client.get(
        "/xlapp_data?session_id=827629574cfb3dcc4a0fdcbf6da4bd89&type=all&time_start=2019-07-01 00:00:00&time_end=2029-07-08 23:00:00")



class UserBehavior(TaskSet):
    tasks = {index: 1}


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000

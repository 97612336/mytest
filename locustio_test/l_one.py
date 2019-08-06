from locust import HttpLocust, TaskSet


def index(l):
    l.client.get("/goods?kind=0&page=1")


class UserBehavior(TaskSet):
    tasks = {index: 1}


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000

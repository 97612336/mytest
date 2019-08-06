from locust import HttpLocust, TaskSet, task


def index(l):
    l.client.get("http://www.xbiquge.la/")


class UserTasks(TaskSet):
    # 列出需要测试的任务形式一
    tasks = [index]

    # 列出需要测试的任务形式二
    @task
    def page404(self):
        self.client.get("/does_not_exist")


class WebsiteUser(HttpLocust):
    host = "http://127.0.0.1:8089"
    min_wait = 2000
    max_wait = 5000
    task_set = UserTasks

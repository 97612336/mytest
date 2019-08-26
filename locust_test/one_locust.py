import json

from locust import HttpLocust, TaskSet, task


class WebsiteTasks(TaskSet):
    @task
    def index(self):
        self.client.post("/xlapp_data", json.dumps({
            "session_id": '827629574cfb3dcc4a0fdcbf6da4bd89',
            "type": 0,
            "data": [
                {"type": "sleep", "value": 1, "time_start": "2019-07-08 08:00:00", "time_end": "2019-07-08 09:00:00"},
                {"type": "heart_bpm", "value": 85, "time_start": "2019-07-08 16:00:00",
                 "time_end": "2019-07-08 17:00:00"}]
        }))

    @task
    def about(self):
        self.client.get(
            "/xlapp_data?session_id=827629574cfb3dcc4a0fdcbf6da4bd89&type=all&time_start=2019-07-01 00:00:00&time_end=2029-07-08 23:00:00")


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 15000

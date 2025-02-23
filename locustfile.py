from locust import HttpUser, between, task


class OrderProcessingUser(HttpUser):
    wait_time = between(1, 2)

    @task(2)
    def create_order(self):
        self.client.post("/order/create_order", json={
            "item_ids": [1, 112],
            "total_amount": 200.0,
            "user_id": 78
        })

    @task(1)
    def get_order(self):
        res = self.client.get("/order/get_order/2230")
        print(res)

    @task(1)
    def get_metrics(self):
        self.client.get("/metrics")


# To start load testing
# locust -f locustfile.py --host=http://127.0.0.1:8000

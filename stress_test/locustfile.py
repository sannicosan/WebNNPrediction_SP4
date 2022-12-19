from locust import HttpUser, task, between


class APIUser(HttpUser):

    # Put your stress tests here.
    # See https://docs.locust.io/en/stable/writing-a-locustfile.html for help.
    # DONE
    wait_time = between(1,5)
    
    @task(1)
    def index(self):
        self.client.get('http://localhost/')
        
    @task(2)
    def predict(self):
        
        # files = ('file', (open('', 'rb'),'dog.jpeg') )
        files = [   ("file", 
                    ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg") ) ]
        
        headers = {}
        payload = {}
        
        self.client.post(  'http://localhost/predict',
                            headers = headers,
                            data = payload,
                            files = files            )
        
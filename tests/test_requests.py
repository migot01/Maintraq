import unittest
import json
from app import app
from app.views import request_model



class RequeststestCase(unittest.TestCase):

    def setUp(self):
        """
        will be called before every test
        """
        self.app = create_app (config_name= 'testing')
        self.client = self.app.test_client
        self.empty_request = {"tittle":"",
              "location": "",
              "body": ""
              }

        self.request={
            "title":"maintenance",
              "location": "nairobi",
              "body": "My laptop requires repair"
        }

        self.update_request = {
            "title":"",
              "location": "",
              "body": ""

        }

    

    def test_request_can_create_successfully(self):
        initial_count = len(request_model.requests)
        res = self.client().post('/api/v1/requests',data = json.dumps(self.request),
                                  headers = {"content-type":"application/json"})
        final_count = len(request_model.requests)
        self.assertEqual (res.status_code, 201)
        self.assertEqual(final_count-initial_count,1)
        self.assertIn("request created",str(res.data))

    def test_cannot_create_name(self):
        """
        Tests that the title ,location and body must be provided to create a new request
         """
        res = self.client().post('/api/v1/requests', data=json.dumps(self.empty_request),
                                  headers = {"content-type":"application/json"})
        assert b'{\n "message":"name cannot be empty!"\n}n' in res.data
    def request_can_be_updated(self):
        old= self.client().post('/api/v1/request' ,data = json.dumps(self.request),
                                  headers = {"content-type":"application/json"})

        new = self.client().put('/api/v1/request/1' , data = json.dumps(self.update_request),
                                 headers = {"content-type": "application/json"})
        self.assertEqual(new.status_code, 202)
        self.assertEqual("request updated!", str(new.data))

    def test_can_get_requests(self):
        """test can get all requests"""
        self.client().post('/api/v1/request' , data = json.dumps(self.request),
                       headers = {"content-type":"application/json"})
        res = self.client().get('/api/v1/requests')
        self.assertEqual(len(request_model.requests),1)



 
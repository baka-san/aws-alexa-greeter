#import greeting 
import greeting_ask as greeting
import unittest
import json


class GreetingTestCase(unittest.TestCase):

    def setUp(self):
      self.app = greeting.app.test_client()

    def tearDown(self):
      pass

    def test_hello_intent(self):

      with open('event.json') as data_file:
        json_data = json.load(data_file)

      req= self.app.post('/alexa_end_point', data=json.dumps(json_data), content_type='application/json')

if __name__ == '__main__':
    unittest.main()

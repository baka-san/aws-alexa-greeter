import greeter_ask as greeter
import unittest
import json


class GreeterTestCase(unittest.TestCase):

    def setUp(self):
      self.app = greeter.app.test_client()
      greeter.app.config['ASK_VERIFY_REQUESTS'] = False
      # greeter.ask.ask_verify_requests = False

    def tearDown(self):
      pass

    def test_hello_intent(self):

      with open('event.json') as data_file:
        json_data = json.load(data_file)

      response = self.app.post('/alexa_end_point', data=json.dumps(json_data), content_type='application/json')
      response = json.loads(response.data)

      self.check_valid_response(response)
      self.assertTrue(response['response']['shouldEndSession'])
      self.assertRegexpMatches(response['response']['outputSpeech']['ssml'], r'<speak>Hello', "Check output speech content")
      self.assertNotIn('reprompt',response['response'], "Shouldn't be reprompt for HelloIntent")

    def test_launch_intent(self):

      with open('event.json') as data_file:
        json_data = json.load(data_file)

      json_data['request']['type'] = 'LaunchRequest'
      json_data['request']['intent'] = {}

      response = self.app.post('/alexa_end_point', data=json.dumps(json_data), content_type='application/json')
      response = json.loads(response.data)

      self.check_valid_response(response)
      self.assertFalse(response['response']['shouldEndSession'], "Shouldn't end session")
      self.assertRegexpMatches(response['response']['outputSpeech']['ssml'], r'<speak>Welcome', "Check output speech content")
      self.assertIn('reprompt',response['response'], "Should be reprompt")

    def check_valid_response(self, response):
      self.assertEqual(response['version'], '1.0', "version?")
      self.assertEqual(response['response']['outputSpeech']['type'], 'SSML', "output speech is SSML?")
      self.assertIsInstance(response['response'], dict, "Response is a dictionary/hash")
      self.assertIsInstance(response['response']['outputSpeech'], dict, "Output speech is a dictionary/hash")
      self.assertIsNotNone(response['response']['shouldEndSession'], "The session hash is not empty")

if __name__ == '__main__':
    unittest.main()

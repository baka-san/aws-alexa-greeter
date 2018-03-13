import greeter_ask as greeter
import unittest
import json


class GreeterTestCase(unittest.TestCase):

    def setUp(self):
      self.app = greeter.app.test_client()
      greeter.app.config['ASK_VERIFY_REQUESTS'] = False
      # greeter.ask.ask_verify_requests = False
      with open('event.json') as data_file:
        self.json_data = json.load(data_file)

    def tearDown(self):
      pass

    def get_response(self, json_data):
      response = self.app.post('/alexa_end_point', data=json.dumps(json_data), content_type='application/json')
      response = json.loads(response.data)
      return response

    def test_01_launch_intent(self):
      json_data = self.json_data.copy()
      json_data['request']['type'] = 'LaunchRequest'
      json_data['request']['intent'] = {}
      response = self.get_response(json_data)

      self.check_valid_response(response, end_session=False)
      self.assertRegexpMatches(response['response']['outputSpeech']['ssml'],r'<speak>Welcome.*</speak>', 'Output speech text check')

    def test_02_hello_intent(self):
      json_data = self.json_data.copy()
      response = self.get_response(json_data)

      self.check_valid_response(response)
      self.assertRegexpMatches(response['response']['outputSpeech']['ssml'],r'<speak>Hello.*</speak>', 'Output speech text check')

    def test_03_quote_intent(self):
      json_data = self.json_data.copy()
      json_data['request']['intent']['name'] = 'QuoteIntent'
      json_data['request']['intent']['slots'] = {}
      response = self.get_response(json_data)

      self.check_valid_response(response, end_session=False)
      GreeterTestCase.prev_response = response
      self.assertRegexpMatches(response['response']['outputSpeech']['ssml'],r'<speak>.*Do you.*</speak>', 'Output speech text check')
      self.assertRegexpMatches(response['response']['reprompt']['outputSpeech']['ssml'],r'<speak>.*You can say.*</speak>', 'Output speech text check')

    def check_valid_response(self, response, end_session=True):
      self.assertEqual(response['version'], '1.0', "version?")
      self.assertEqual(response['response']['outputSpeech']['type'], 'SSML', "output speech is SSML?")
      self.assertIsInstance(response['response'], dict, "Response is a dictionary/hash")
      self.assertIsInstance(response['response']['outputSpeech'], dict, "Output speech is a dictionary/hash")
      self.assertIsNotNone(response['response']['shouldEndSession'], "The session hash is not empty")
      self.assertRegexpMatches(response['response']['outputSpeech']['ssml'], r'<speak>.*</speak>', "Check output speech content")
      if end_session:
        self.assertTrue(response['response']['shouldEndSession'])
        self.assertNotIn('reprompt',response['response'], "Shouldn't have reprompt")
      else:
        self.assertFalse(response['response']['shouldEndSession'], "Shouldn't end session")
        self.assertIn('reprompt',response['response'], "Should have reprompt")
        self.assertRegexpMatches(response['response']['reprompt']['outputSpeech']['ssml'], r'<speak>.*</speak>', "Check output speech content")


if __name__ == '__main__':
    unittest.main()

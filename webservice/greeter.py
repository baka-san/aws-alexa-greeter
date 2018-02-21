from flask import Flask
from flask import request
from flask import make_response
import json
import datetime
import os
import logging

app = Flask(__name__)

@app.route('/')
def hello():
  return 'Hello World!'

@app.route('/alexa_end_point', methods=['POST'])
def alexa():
  event = request.get_json()

  print('\nREQUEST:\n')
  print json.dumps(event, indent=2, sort_keys=True)

  req = event['request']

  if req['type'] == 'LaunchRequest':
    return handle_launch_request()

  elif req['type'] == 'IntentRequest':
    if req['intent']['name'] == 'HelloIntent':
      # print(handle_hello_intent(req))
      # print("start")
      # print(message['response'])
      # print("end")

      return handle_hello_intent(req)
    # elif req['intent']['name'] == 'QuoteIntent':
    #   return handle_quote_intent()
    # elif req['intent']['name'] == 'NextQuoteIntent':
    #   return handle_next_quote_intent()
    # elif req['intent']['name'] == 'AMAZON.StopIntent':
    else:
      return "Bad Request", 400

  elif req['type'] == 'SessionEndedRequest':
    pass


def handle_hello_intent(req):
  """Handles hello intent and generates a response"""

  name = req['intent']['slots']['FirstName']['value']
  res = Response()
  res.speech_text = "Hello {0} .".format(name)
  res.speech_text += " That\'s spelt as <say-as interpret-as='spell-out'>{0}</say-as>, isn\'t it?".format(name)
  res.speech_text += get_greeting()

  return res.build_response()

def get_greeting():
  """Returns the proper greeting based on what time it is"""

  current_time = datetime.datetime.utcnow()
  hours = current_time.hour + 9

  if hours < 0:
    hours += 24

  if hours < 12:
    return "Good morning."
  elif hours < 18:
    return "Good afternoon."
  else: 
    return "Good evening."


def handle_launch_request():
  """Handles launch request and generates response"""
  res = Response()

  res.speech_text = "Welcome to Greetings skill. Using this skill you can greet your guests. Who do you want to greet?"
  res.reprompt_text = "For example, you can say hello to John. Who would you like to greet?"
  res.end_session = False

  return res.build_response()


class Response(object):
  """Alexa skill response object with helper functions"""

  def __init__(self):
    self.speech_text = None
    self.reprompt_text = None
    self.end_session = True

  def build_response(self):
    """Builds alexa response and returns"""

    fnl_res = {
      'version': '1.0',
      'response': {
        'outputSpeech': {
          'type': 'SSML',
          'ssml': '<speak>{0}</speak>'.format(self.speech_text)
        },
        'shouldEndSession': self.end_session
      }
    }

    if self.reprompt_text:
      fnl_res['response']['reprompt_text'] = {
        'outputSpeech': {
          'type': 'SSML',
          'ssml': '<speak>{0}</speak>'.format(self.reprompt_text)
        }
      }

    print('\nRESPONSE:\n')
    print json.dumps(fnl_res, indent=2, sort_keys=True)

    http_response = make_response(json.dumps(fnl_res))
    http_response.headers['Content-Type'] = 'application/json'
    return http_response

if __name__ == '__main__':
  # app.run(debug=True)
  port = int(os.getenv('PORT', 5000))
  print "Starting app on port %d" % port
  app.run(debug=False, port=port, host='0.0.0.0')



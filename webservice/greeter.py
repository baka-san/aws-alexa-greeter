from flask import Flask
from flask import request
from flask import make_response
import json
import datetime

app = Flask(__name__)

@app.route('/')
def hello():
  return 'Hello World!'

@app.route('/alexa_end_point', methods=['POST'])
def alexa():
  event = request.get_json()

  print('\nREQUEST:\n')
  print(event)

  req = event['request']

  if req['type'] == 'LaunchRequest':
    return handle_launch_request()

  elif req['type'] == 'IntentRequest':
    if req['intent']['name'] == 'HelloIntent':
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
  response = Response()
  response.speechText = "Hello {0} . ".format(name)
  response.speechText += "That\'s spelt as <say-as interpret-as='spell-out'>{0}</say-as>, isn\'t it?".format(name)
  response.speechText += get_greeting()

  return response.build_response()

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
  response = Response()

  response.speechText = "Welcome to Greetings skill. Using this skill you can greet your guests. Who do you want to greet?"
  response.repromptText = "For example, you can say hello to John. Who would you like to greet?"
  response.endSession = false

  return response.build_response()


class Response(object):
  """Alexa skill response object with helper functions"""

  def __init__(self):
    self.speech_text = None
    self.reprompt_text = None
    self.end_session = True

  def build_response(self):
    """Builds alexa response and returns"""

    response = {
      'version': '1.0',
      'response': {
        'outputSpeech': {
          'type': 'SSML',
          'ssml': '<speak>' + str(self.speech_text) + '</speak>'
        },
        'shouldEndSession': self.end_session
      }
    }

    if self.reprompt_text:
      response['response']['reprompt_text'] = {
        'outputSpeech': {
          'type': 'SSML',
          'ssml': '<speak>' + str(self.reprompt_text) + '</speak>'
        }
      }

    http_response = make_response(json.dumps(response))
    http_response.headers['Content-Type'] = 'application/json'
    return http_response

if __name__ == '__main__':
  app.run()

from flask import Flask
from flask_ask import Ask, statement, question, session
import requests
import datetime
import os
import logging


app = Flask(__name__)
app.config['ASK_APPLICATION_ID'] = 'amzn1.ask.skill.b9e89f5a-1b07-4a77-b662-be72528f9d5c'
ask = Ask(app, '/alexa_end_point')
app.config['ASK_VERIFY_REQUESTS'] = False

if os.getenv('GREETER_DEBUG_EN', False):
  logging.getLogger('flask-ask').setLevel(logging.DEBUG)

@ask.launch
def launch():
  speech_text = get_ssml("Welcome to Greetings skill. Using this skill you can greet your guests. Who do you want to greet?")
  reprompt_text = get_ssml("For example, you can say hello to John. Who would you like to greet?")
  return question(speech_text).reprompt(reprompt_text)

@ask.intent('HelloIntent', mapping={'first_name': 'FirstName'}, default={'first_name': 'Unknown'})
def hello(first_name):
  speech_text = "Hello {0} .".format(first_name)
  speech_text += " That\'s spelt as <say-as interpret-as='spell-out'>{0}</say-as>, isn\'t it? ".format(first_name)
  speech_text += get_greeting()
  speech_text += " Here's a nice quote for you: "
  speech_text += get_quote()
  # get_quote()
  return statement(get_ssml(speech_text))
  # .standard_card('Hello {}'.format(first_name), quote, small_image_url='https://upload.wikimedia.org/wikipedia/commons/5/5b/Hello_smile.png', large_image_url='https://upload.wikimedia.org/wikipedia/commons/5/5b/Hello_smile.png')


@ask.intent('QuoteIntent')
def quote_intent():
  speech_text, reprompt_text = get_quote_text()
  session.attributes['quote_intent'] = True
  return question(speech_text).reprompt(reprompt_text)

def get_quote_text():
  speech_text = get_quote()
  speech_text += ' Do you want to listen to one more quote? ' 
  reprompt_text = 'You can say yes or one more. '
  speech_text = get_ssml(speech_text)
  reprompt_text = get_ssml(reprompt_text)
  return speech_text,reprompt_text

@ask.intent('NextQuoteIntent')
def next_quote_intent():
  if 'quote_intent' in session.attributes:
    speech_text,reprompt_text = get_quote_text()
    return question(speech_text).reprompt(reprompt_text)
  else:
    speech_text = get_ssml('Wrong invocation of this intent. Please say get me a quote to get quote.')
    return statement(speech_text)

@ask.session_ended
def session_ended():
  return "", 200

def get_quote():
  req = requests.get('http://api.forismatic.com/api/1.0/json?method=getQuote&lang=en&format=json')
  # print("req")
  # print(req.content)
  req._content = req._content.replace('\\',"")
  quote = req.json()['quoteText']
  return quote

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

def get_ssml(msg):
  return '<speak>{}</speak>'.format(msg)


if __name__ == '__main__':
  # if 'ASK_VERIFY_REQUESTS' in os.environ:
  #     verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
  #     if verify == 'false':
  #       app.config['ASK_VERIFY_REQUESTS'] = False
  app.run()



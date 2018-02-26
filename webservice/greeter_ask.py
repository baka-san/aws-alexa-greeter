from flask import Flask
from flask_ask import Ask, statement, question
import requests
import datetime
import os
import logging


app = Flask(__name__)
ask = Ask(app, '/alexa_end_point')
# app.config['ASK_VERIFY_REQUESTS'] = False

@ask.launch

def launch():
  speech_text = "<speak>Welcome to Greetings skill. Using this skill you can greet your guests. Who do you want to greet?</speak>"
  reprompt_text = "<speak>For example, you can say hello to John. Who would you like to greet?</speak>"
  return question(speech_text).reprompt(reprompt_text)

@ask.intent('HelloIntent', mapping={'first_name': 'FirstName'}, default={'first_name': 'Unknown'})
def hello(first_name):
  speech_text = "Hello {0} .".format(first_name)
  speech_text += " That\'s spelt as <say-as interpret-as='spell-out'>{0}</say-as>, isn\'t it? ".format(first_name)
  speech_text += get_greeting()
  speech_text += " Here's a nice quote for you: "
  speech_text += get_quote()
  # get_quote()
  return statement('<speak>{}</speak>'.format(speech_text))

  # .standard_card('Hello {}'.format(first_name), quote, small_image_url='https://upload.wikimedia.org/wikipedia/commons/5/5b/Hello_smile.png', large_image_url='https://upload.wikimedia.org/wikipedia/commons/5/5b/Hello_smile.png')

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


if __name__ == '__main__':
  # if 'ASK_VERIFY_REQUESTS' in os.environ:
  #     verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
  #     if verify == 'false':
  #       app.config['ASK_VERIFY_REQUESTS'] = False
  app.run()



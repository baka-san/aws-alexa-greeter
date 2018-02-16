"use strict"
var http = require("http")

exports.handler = function(event, context) {

  try {
    var request = event.request
    var session = event.session

    if (!event.session.attributes) {
      event.session.attributes = {}
    }

    if (request.type === "LaunchRequest") {
      handleLaunchRequest(context)
    }
    else if (request.type == "IntentRequest") {
      if (request.intent.name === "HelloIntent") {
        handleHelloIntent(request, context)
      }
      else if (request.intent.name === "QuoteIntent") {
        handleQuoteIntent(request, context, session)
      }
      else if (request.intent.name === "NextQuoteIntent") {
        handleNextQuoteIntent(request, context, session)
      }
      else {
        throw "Unknown intent"
      }
    }
    else if (request.type == "SessionEndedRequest") {

    }
    else {
      throw "Unknown intent"
    }
  }
  catch(e) {
    context.fail("Exception: " + e)
  }

}


function getQuote(callback) {
  var url = "http://api.forismatic.com/api/1.0/json?method=getQuote&lang=en&format=json"
  var req = http.get(url, function(res) {
    var body = ""

    res.on("data", function(chunk){
      body = body.replace(/\\/g,"")
      body += chunk
    })

    res.on("end", function(){
      var quote = JSON.parse(body)
      callback(quote.quoteText)
    })

  })

  req.on("error", function(err){
    callback("", err)
  })
}

function getGreeting() {
  var myDate = new Date()
  var hours = myDate.getUTCHours() + 9

  if (hours < 0) {
    hours = hours + 24
  }

  if (hours < 12) {
    return "Good morning."
  }
  else if (hours < 18) {
    return "Good afternoon."
  }
  else {
    return "Good evening."
  }
}

function buildResponse(options) {
  var response = {
    version: "1.0",
    response: {
      outputSpeech: {
        type: "SSML",
        ssml: "<speak>" + options.speechText + "</speak>"
      },
      shouldEndSession: options.endSession
    }
  }

  if (options.repromptText) {
    response.response.reprompt = {
      outputSpeech: {
        type: "SSML",
        ssml: "<speak>" + options.repromptText + "</speak>"
      }
    }
  }

  if (options.session && options.session.attributes) {
    response.sessionAttributes = options.session.attributes
  }
  
  return response  
}


function handleLaunchRequest(context) {
  let options = {}
  options.speechText = "Welcome to Greetings skill. Using this skill you can greet your guests. Who do you want to greet?"
  options.repromptText = "For example, you can say hello to John. Who would you like to greet?"
  options.endSession = false;

  context.succeed(buildResponse(options))
}

function handleHelloIntent(request, context) {
  let options = {}
  let name = request.intent.slots.FirstName.value
  options.speechText = `Hello ${name}. ` + getGreeting()
  options.speechText += ` That\'s spelt as <say-as interpret-as="spell-out">${name}</say-as>, isn\'t it?`
  getQuote(function(quote, err){
    if (err) {
      context.fail(err)
    }
    else {
      options.speechText += ` Here\'s a nice quote for you: ${quote}`
      options.endSession = true;
      context.succeed(buildResponse(options))
    }
  })
}

handleQuoteIntent(request, context, session) {
  let options = {}
  options.session = session

  getQuote(function(quote, err){
    if (err) {
      context.fail(err)
    }
    else {
      options.speechText = ` Here\'s a nice quote for you: ${quote}`
      options.speechText += ` Do you want to listen to one more quote?`
      options.repromptText = " You can say yes or one more."
      options.session.attributes.quoteIntent = true;
      options.endSession = false;
      context.succeed(buildResponse(options))
    }
  })
}

handleQuoteIntent(request, context, session) {
  let options = {}

  if (session.attributes.quoteIntent) {
    getQuote(function(quote, err){
      if (err) {
        context.fail(err)
      }
      else {
        options.speechText = ` Here\'s a nice quote for you: ${quote}`
        options.speechText += ` Do you want to listen to one more quote?`
        options.repromptText = " You can say yes or one more."
        options.endSession = false;
        context.succeed(buildResponse(options))
      }
    })
  }
  else {
    options.speechText = "Wrong invocation of this intent"
    options.endSession = true
  }

}
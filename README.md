# AWS Alexa Greeter

### Section 1: Greeter skill using an AWS Lambda function  
#### **Code found at:** 

**Description**  
A skill called Greeter was created on [developer.amazon](https://developer.amazon.com/). The function code was executed using a Lambda function found on [console.aws.amazon](console.aws.amazon.com). The code was written with Node.js and tested using the Mocha test framework.

The code can be invoked with phrases such as: 


> Ask Greeter to say hello to John.  
> Ask Greeter to greet our guest John.  
> Ask Greeter to greet John.

This will return a response like:

> Hello John, good morning. That's spelt J-O-H-N, isn't it? Here's a nice quote for you: *Zombies eat brains so you're safe.*

You can get another quote with phrases such as:
> Ask Greeter to get me a quote.  
> Ask Greeter to get a quote.

Greeter will ask you if you'd like to hear another quote. You can respond with phrases such as:

> More  
> One more  
> Yes  
> No
> Stop

Both simple and standard [cards](https://developer.amazon.com/docs/custom-skills/include-a-card-in-your-skills-response.html) (i.e. has an image) are available to be viewed on appropriate devices.

### Section 2: Greeter skill using a web service as an end point
#### **Code found at:** 


**Description**  
Code was written with Python and the Flask web framework. The site can be deployed both local web server like Ngrok or on a Heroku.


See the full tutorial on [Udemy](https://www.udemy.com/comprehensive-alexa-skill-development-course/learn/v4/overview).
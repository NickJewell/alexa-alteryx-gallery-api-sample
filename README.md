
README

This is a simple repository that contains SOME of the code components needed by the Alexa skill in order to call a parameterised analytic app from the Alteryx Gallery. 

Due to size constraints on some of the larger libraries, I'll list out which python libraries you need to use below:

 - pandas 
 - numpy
 - pyryx
 - requests
 - oauthlib
 - six

Use a command such as:
**pip install --target=d:\somewhere\other\than\the\default package_name** to get local copies of these packages which can then be bundled into your lambda function. 

HOW TO DEPLOY

Download this repository and the index.py file. Feel free to edit the contents of index.py to meet your needs, and to include the relevant Alteryx Server API credentials, server location and Alexa Skill ID (when ready). 

Zip these files locally so that you can import them into your AWS Lambda function as a single package (or host them in a dedicated S3 bucket - for the size of the zip file needed here (around 33Mb) I'd recommend S3). 

Create your AWS Lambda function by signing up at: https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions

Create your Alexa Skill by signing up at: 
https://developer.amazon.com/alexa-skills-kit

Test your skill using: 
http://echosim.io/

CONFIGURATION NOTES:
--------------------

LAMBDA FUNCTION Configuration: 

 - Be sure to use a blank python function template
 - Use Python 2.7
 - Set your handler to alexa-promote.lambda_handler (referencing the python code in the repo)
 - You'll need to create a basic lambda execution role. Instructions here: http://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-create-iam-role.html
 - In Advanced Settings, use a timeout of 30s (as I've found the default 3s to be a little unforgiving!)
 - Once created, take a note of the ARN (Amazon Resource ID) as you'll need to link this into your Alexa Skill.

ALEXA SKILL Configuration: 

 - Add a new skill via the developer console at: https://developer.amazon.com/edw/home.html#/skills
 - Once created, make sure you note the skill ID (you then need to add this to your lambda function) 
 - Give the skill a name. For example 'Alteryx-Gallery-Demo-1'
 - Give the skill an invocation, for example 'gallery analytics'. This means you'll call the skill by saying 'Alexa, open gallery analytics'
 - Define an Interaction Model. For this example, we've added some extra slots to capture the model parameters we want to use for scoring. An interesting issue with the built-in Alexa SLOT_TYPES means that it can't read decimals using AMAZON.NUMBER, so we have a more complex interaction model that handles pre-decimal and post-decimal numbers for this example. 
 
> {
  "intents": [
    {
      "slots": [
        {
          "name": "ProductType",
          "type": "LIST_OF_CATEGORIES"
        }
      ],
      "intent": "AlteryxAPIParameter"
    },
    {
      "intent": "AMAZON.HelpIntent"
    }
  ]
}


 - Set up Sample Utterances so that the skill knows how to run. In our Python code we're expecting an Intent called AlteryxAPIParameter, so add a sample such as:
> AlteryxAPIParameter pull total sales for {ProductType}

 - So when the user says 'Alexa, ask gallery analytics to pull total sales for office supplies', the correct python function will trigger. 
 - We've used a custom SLOT_TYPE called LIST_OF_CATEGORIES - set this up with the following values: Furniture | Office Supplies | Technology
 - Go to the configuration tab, and make sure that the ARN for the Lambda code is entered here. 
 - Now go to the test tab, and start trying the skill out! If you get errors, go back to your AWS console and examine the Cloudwatch logs: you'll get all the python log details there. Also, check your Alteryx Server logs in case the analytic app itself is having issues. 


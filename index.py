"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6
For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
             "YOURAMAZONSKILLID"):
         raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "CallAlteryxAPI":
        return call_api(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


		
	
	
def call_api(intent, session):
    """ Processes a call to the Alteryx Gallery API
    """
    import sys
    import pyryx
    import pandas as pd    

    # Gallery API keys and location	
	
    client_key = 'GALLERY_CLIENT_KEY'
    client_secret = 'GALLERY_SECRET_KEY'
    gallery_url = 'GALLERY_URL_API_ENDPOINT'

    # Handle to Alteryx API	
	
    ayx = pyryx.PyRyxApi(client_key, client_secret, gallery_url)	

    # Determining and Defining App Questions
	
    questions_list = ayx.getWorkflowQuestions('WORKFLOW_ID')
	
    questions = [{ "name": question['name']} for question in questions_list]

    category = 'Office Supplies'	
	
    questions[0]['value'] = category	
	
    question_param = { "questions" : questions }	

    # Retrieve and format job results	
	
    jobs = ayx.getWorkflowJobs('WORKFLOW_ID')	

    latest_job_id = jobs[-1]['id']	
	
    job_output_id = ayx.checkJobState(latest_job_id)['outputs'][0]['id']	
	
    df = ayx.getJobOutput(latest_job_id, job_output_id)	
    val = df['TotalSpend'][0]	
    val_out = "%0.2f" % val	
	
    speech_output = "Total Sales for the " + category + " category is $" + val_out	
	
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    reprompt_text = "This shouldn't happen"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
	
	
# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Alteryx Gateway. " \
                    "Please tell me what data you wish to retrieve, " \
                    "for example, get my sales forecast. " \
                    "Also, please allow a few seconds for the results to be accessed. " \
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what data you wish to retrieve, " \
                    "for example, get my sales forecast"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

		
		
		
# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
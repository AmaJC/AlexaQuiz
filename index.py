import response_builder
import quizquestion
import random

# Handler for launch, intent, and session ended Requests. 
# This function routes the incoming request based on type (LaunchRequest,
# IntentRequest, etc.) The JSON body of the request is provided in the event parameter.
def handler(event, context):
    if event['session']['new']:
        on_session_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return on_intent_request(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_end()
    return on_intent_request(event)

# Called when the session starts.
def on_session_start():
    print("Session Started.")

# Called when the user invokes the skill.
def on_launch(event):
    welcome_message = "Welcome to Where In The World Europe edition! I will ask you " + NUM_GAME_QUESTIONS \
            + " questions, try to get as many right as you can. Just say your best guess. Let's start. "
    reprompt_message = "Try to get as many questions right as you can."
    card_text = "Respond with your best guess for each question."
    card_title = "Welcome to WhereInTheWorld!"

    game_info = {"questions" : populate_game_questions(), "current_q_index" : 0, "score" : 0}
    welcome_message += game_info["questions"][0][0]
    return response_builder.build_json_response(welcome_message, card_text, card_title, reprompt_message, game_info, False)

################################################################################################################################
# TESTING choosing gamemode, rapid fire vs specific
def on_launch(event):
    welcome_message = "Welcome to Where In The World Europe edition! Do you want rapid fire mode or mastery mode?"
    reprompt_message = "Try to get as many questions right as you can."
    card_text = "Rapid fire or mastery mode?"
    card_title = "Welcome to WhereInTheWorld!"

    if GAME_MODE==RapidFire:
        game_info = {"questions" : populate_game_questions("all"), "current_q_index" : 0, "score" : 0}
        welcome_message += game_info["questions"][0][0]
        return response_builder.build_json_response(welcome_message, card_text, card_title, reprompt_message, game_info, False)
    else:
        welcome_message="Which country would you like to master? England, France, or Germany?"
        if USER_RESPONSE=="England":
            game_info = {"questions" : populate_game_questions("England"), "current_q_index" : 0, "score" : 0}
            return response_builder.build_json_response(welcome_message, card_text, card_title, reprompt_message, game_info, False)
        elif USER_RESPONSE=="France":
            game_info = {"questions" : populate_game_questions("France"), "current_q_index" : 0, "score" : 0}
            return response_builder.build_json_response(welcome_message, card_text, card_title, reprompt_message, game_info, False)
        elif USER_RESPONSE=="Germany":
            game_info = {"questions" : populate_game_questions("Germany"), "current_q_index" : 0, "score" : 0}
            return response_builder.build_json_response(welcome_message, card_text, card_title, reprompt_message, game_info, False)
################################################################################################################################


def on_session_end():
    print("Session Ended.")

# Called when a user input is mapped by Alexa to an intent
def on_intent_request(event):
    intent_name = event['request']['intent']['name']
    if intent_name == "AnswerIntent":
<<<<<<< Updated upstream
    	return handleAnswerRequest(event)
    # elif intentName == "DontKnowIntent":
    #     handleDontKnowRequest(event)

def handleAnswerRequest(event):
	user_answer = event['request']['intent']['slots']['Capital']['value']
	all_game_questions = event['session']['attributes']['questions']
	
	question_number = event['session']['attributes']["current_q_index"]
	if user_answer == all_game_questions[question_number][1]:
		event['session']['attributes']["score"] += 1
		return response_builder.build_json_response(user_answer + " is correct!", "","","", "", False)
	else:
		return response_builder.build_json_response(user_answer + " is incorrect! You suck.", "","","", "", False)
	#next_question = all_game_questions[question_number + 1]
	
	
	#if user_answer == all_game_questions[question_number][1]:
		#event['sessionAttributes']["score"] += 1
		#return response_builder.build_json_response(user_answer + " is correct!" + next_question, "","","", event['session']['attributes'], False)
	#return response_builder.build_json_response(user_answer + " is incorrect!" + next_question, "","","", event['session']['attributes'], False)

def handleDontKnowRequest(event):
    return response_builder.build_json_response("You suck. Next question", "","","", "", False)
=======
        return handle_answer(event)
    elif intent_name == "DontKnowIntent":
        return handle_dont_know(event)
    elif intent_name == "AMAZON.NoIntent":
        return handle_no(event)
    elif intent_name == "AMAZON.YesIntent":
        return handle_yes(event)
    elif intent_name == "AMAZON.RepeatIntent":
        return handle_repeat(event)
    elif intent_name == "AMAZON.HelpIntent":
        return handle_help(event)
    elif intent_name == "AMAZON.NavigateHomeIntent":
        return on_launch()
    elif intent_name == "AMAZON.CancelIntent":
        return handle_stop(event)
    elif intent_name == "AMAZON.StopIntent":
        return handle_stop(event)
    else:
        session_attributes = event['session']['attributes']
        if not event['request']['intent']['slots']:
            # unrecognized answer
            event['request']['intent']['slots'] = {"Answer": ""}
            return handle_answer(event)

def handle_answer(event):
    if not has_session_attributes(event) or 'questions' not in event['session']['attributes']:
        # If the user responded with an answer but there is no game in progress, ask the user
        # if they want to start a new game. Set a flag to track that we've prompted the user.
        return ask_to_start_a_new_game()
    session_attributes = event['session']['attributes']
    curr_q_ind = session_attributes["current_q_index"]
    if curr_q_ind >= int(NUM_GAME_QUESTIONS):
        return ask_to_start_a_new_game()
    user_answer = event['request']['intent']['slots']['Answer']['value']
    game_questions = session_attributes['questions']

    if user_answer.upper() == game_questions[curr_q_ind][1].upper():
        session_attributes["score"] += 1
        result = "correct!"
    else:
        result = "incorrect."
    
    session_attributes["current_q_index"] += 1
    if session_attributes["current_q_index"] < int(NUM_GAME_QUESTIONS):
        next_q = game_questions[curr_q_ind + 1][0]
        next_q_response = " Next question. {0}".format(next_q)
        if result=="correct!":
            answer_result = "{0} is {1}".format(user_answer, result)
            return response_builder.build_json_response(answer_result + next_q_response, next_q_response, "", next_q_response, session_attributes, False)
        else:
            answer_result = "Incorrect! {0} is correct.".format(game_questions[curr_q_ind][1].upper())
            return response_builder.build_json_response(answer_result + next_q_response, next_q_response, "", next_q_response, session_attributes, False)
    else:
        score = session_attributes["score"]
        session_attributes["user_prompted_to_start"] = True
        return response_builder.build_json_response("{0} is {1}. Game over! You got {2} out of {3} questions correct. Want to play again?".format(user_answer, result, score, NUM_GAME_QUESTIONS), "", "", "Game over! Want to play again?", session_attributes, False)

def handle_dont_know(event):
    if not has_session_attributes(event):
        return ask_to_start_a_new_game()
    session_attributes = event['session']['attributes']
    if "user_prompted_to_start" in session_attributes and session_attributes["user_prompted_to_start"]:
        return handle_on_session_end_request(event)
    if "user_prompted_to_continue" in session_attributes and session_attributes["user_prompted_to_continue"]:
        return handle_on_session_end_request(event)

    session_attributes = event['session']['attributes']
    game_questions = session_attributes['questions']
    curr_q_ind = session_attributes["current_q_index"]

    answer_pass_response = "The correct answer is {0}.".format(game_questions[curr_q_ind][1])

    session_attributes["current_q_index"] += 1
    if session_attributes["current_q_index"] < int(NUM_GAME_QUESTIONS):
        next_q = game_questions[curr_q_ind + 1][0]
        next_q_response = "{0} Next question. {1}".format(answer_pass_response, next_q)
        return response_builder.build_json_response(next_q_response, "", "", next_q_response, session_attributes, False)
    else:
        score = session_attributes["score"]
        session_attributes = {"user_prompted_to_start" : True}
        return response_builder.build_json_response("{0} Game over! You got {1} out of {2} questions correct. Want to play again?".format(answer_pass_response,score, NUM_GAME_QUESTIONS), "", "", "Game over! Want to play again?", session_attributes, False)

def handle_repeat(event):
    if not has_session_attributes(event):
        return ask_to_start_a_new_game()
    session_attributes = event['session']['attributes']
    if "user_prompted_to_start" in session_attributes and session_attributes["user_prompted_to_start"]:
        return ask_to_start_a_new_game(event)
    if "user_prompted_to_continue" in session_attributes and session_attributes["user_prompted_to_continue"]:
        return handle_help(event)

    session_attributes = event['session']['attributes']
    game_questions = session_attributes['questions']
    curr_q_ind = session_attributes["current_q_index"]
    return response_builder.build_json_response(game_questions[curr_q_ind][0], "", "", game_questions[curr_q_ind][0], session_attributes, False)

def handle_stop(event):
    session_attributes = event['session']['attributes']
    score = session_attributes["score"]
    return response_builder.build_json_response("Game over! You got {0} out of {1} questions correct. Thanks for playing!".format(score, NUM_GAME_QUESTIONS), "", "", "", session_attributes, True)

def handle_no(event):
    if not has_session_attributes(event):
        return ask_to_start_a_new_game()
    session_attributes = event['session']['attributes']
    if "user_prompted_to_start" in session_attributes and session_attributes["user_prompted_to_start"]:
        return handle_on_session_end_request(event)
    if "user_prompted_to_continue" in session_attributes and session_attributes["user_prompted_to_continue"]:
        return handle_on_session_end_request(event)
    else:
        return ask_to_start_a_new_game()

def handle_yes(event):
    if not has_session_attributes(event):
        return ask_to_start_a_new_game()
    session_attributes = event['session']['attributes']
    if 'user_prompted_to_continue' in session_attributes and session_attributes['user_prompted_to_continue']:
        # After being asked "Do you want to keep playing?", user said yes
        game_questions = session_attributes['questions']
        curr_q_ind = session_attributes["current_q_index"]
        next_q = game_questions[curr_q_ind][0]
        del session_attributes['user_prompted_to_continue']
        return response_builder.build_json_response("Next question. {0}".format(next_q), "", "", next_q, session_attributes, False)
    elif 'user_prompted_to_start' in session_attributes and session_attributes['user_prompted_to_start']:
        # After being asked "Do you want to start a new game?", user said yes
        return on_launch()
    else:
        return ask_to_start_a_new_game()

def handle_help(event):
    helpOutput = "I will ask you " + NUM_GAME_QUESTIONS + " geography related questions. " \
        + "Respond with your best guess. " \
        + "To start a new game at any time, say start game. " \
        + "To repeat the last question, say repeat. " \
        + "If you don't know, say skip. " \
        + "Would you like to keep playing?"
    session_attributes = event['session']['attributes']
    if not session_attributes:
        event['session']['attributes'] = {}
    if 'questions' in session_attributes and session_attributes["current_q_index"] >= int(NUM_GAME_QUESTIONS):
        # If user asked for help at the end of the game
        session_attributes['user_prompted_to_start'] = True
    elif 'questions' in session_attributes:
        # If user asked for help in the middle of a game
        session_attributes['user_prompted_to_continue'] = True
    else:
        session_attributes['user_prompted_to_start'] = True
    return response_builder.build_json_response(helpOutput, "Respond to each question with your best guess.", "", helpOutput, session_attributes, False)

def handle_on_session_end_request(event):
    goodbye = "Goodbye for now!"
    return response_builder.build_json_response(goodbye, "Thanks for playing!","","", {}, True)

def ask_to_start_a_new_game():
    session_attributes = {"user_prompted_to_start" : True}
    speech_output = "There is no game in progress. Do you want to start a new game?"
    return response_builder.build_json_response(speech_output, "","", speech_output, session_attributes, False)

def has_session_attributes(event):
    return event['session'] and event['session']['attributes']
>>>>>>> Stashed changes

# SKILL SPECIFIC LOGIC


NUM_GAME_QUESTIONS = '5';

def populate_game_questions(mode):
  """Build and return the list of questions for this game, no duplicates."""
  indices = random.sample(range(0, len(quizquestion.questions_all)), 5) # If user doesn't specify, choose 5 random questions
  return quizquestion.QuizQuestion.get_game_questions(indices)   

print(populate_game_questions()) 


################################################################################################################################
#TESTING populate game questions with modes
def populate_game_questions(mode):
  """Build and return the list of questions for this game, no duplicates."""
  if mode=="all":
    indices = random.sample(range(0, len(quizquestion.questions_all)), 5) # If user doesn't specify, choose 5 random questions
    return quizquestion.QuizQuestion.get_game_questions(indices)
  elif mode=="England":
    indices = random.sample(range(0, len(quizquestion.questions_england)), 5) # If user doesn't specify, choose 5 random questions
    return quizquestion.QuizQuestion.get_game_questions(indices)
  elif mode=="France":
    indices = random.sample(range(0, len(quizquestion.questions_france)), 5) # If user doesn't specify, choose 5 random questions
    return quizquestion.QuizQuestion.get_game_questions(indices)  
  elif mode=="Germany": 
    indices = random.sample(range(0, len(quizquestion.questions_germany)), 5) # If user doesn't specify, choose 5 random questions
    return quizquestion.QuizQuestion.get_game_questions(indices)
print(populate_game_questions()) 
################################################################################################################################
import logging, math

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

from tfl import TFL
from state import State

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

command_config = "Alexa ask bus stop to configure"
command_next_stop = "Alexa ask bus for arrivals"


@ask.launch
def skill_opened():
    state = State(session)
    logging.debug("Current state is ".format(state.load_user_data()))
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("ConfigureIntent")
def configure(is_repeat = False): 
    msg = render_template("configure" if not is_repeat else "configure_repeat" )
    session.attributes['mode'] = "configuration"
    return question(msg)


@ask.intent("ConfigureBusStopIntent", convert={'number_first': int, 'number_second': int, 'number_third': int})
def configure_bus_stop(number_first, number_second, number_third):
    number = ''.join([str(i) for i in [number_first, number_second, number_third] if i != None])
    if session.attributes['mode'] != "configuration":
        return statement("To start configuration say {}".format(command_config))

    logging.debug("Got input from user {}".format(number))
    bus_stop = TFL.lookup_bus_stop(number)

    if bus_stop == None:
        return question("I could not find the bus stop number «{}», please double check number and say it again".format(number))
    
    msg = "I found bus stop called «{}». Is that correct?".format(bus_stop[1])
    session.attributes['naptan_code'] = bus_stop[0]

    return question(msg) #.repromt("I didn't get that. Can you repest the bus stop number clearly again?")



@ask.intent("CommingIntent")
def arrivals():

    busstop = "490012651S"

    arrivals = TFL.arrivals(busstop)
    arrivals = [ "#{} in {}minutes".format(i[0], math.floor(i[1]/60)) for i in arrivals ]
    msg = render_template('arrivals', arrivals=arrivals)

    return statement(msg)


@ask.intent("YesIntent")
def yes():
    state = State(session)
    [current, naptan_code] = [session.attributes['mode'] or None, session.attributes['naptan_code'] or None]
    print("YesIntent got [current, naptan_code]: {}".format([current, naptan_code]))
    if current == "configuration" and naptan_code != None:
        state.update_busstop(naptan_code)
        return statement("Ok, I remembered that. To use say «{}»".format(command_next_stop))

    return statement("Sorry, I didn't get it. Please try to ask me again")

@ask.intent("NoIntent")
def no():
    state = State(session)
    [current, naptan_code] = [session.attributes['mode'] or None, session.attributes['naptan_code'] or None]
    print("NoIntent got [current, naptan_code]: {}".format([current, naptan_code]))
    if (current == "configuration") and (naptan_code != None):
        session.attributes['naptan_code'] = None
        return configure(is_repeat = True)

    return statement("Sorry, I didn't get it. Please try to ask me again")



@ask.session_ended
def session_ended():
    return "Don't be late", 200

@ask.intent("AMAZON.HelpIntent") 
def help():
    return statement("It's a help section. To configure skill say ".format(command_config))

@app.teardown_request
def teardown_request(exception=None):
    pass
#    print("after state {}".format(session.state))

@app.before_request
def before_request():
    pass

if __name__ == '__main__':

    app.run(debug=True)
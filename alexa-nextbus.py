import logging, math

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

from tfl import TFL
from state import State

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def skill_opened():
    state = State(session)
    logging.debug("Current state is ".format(state.load_user_data()))
    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent("SquareIntent", convert={'number': int})
def squareIt(number):
    msg = render_template('square', asked=number, result=number*number)

    return statement(msg)

@ask.intent("ConfigureIntent")
def configure(): 
	msg = render_template("configure")
	return question(msg)


@ask.intent("ConfigureBusStop", convert={'first': int, 'second': int, 'third': int, 'forth': int, 'fifth': int })
def configure_bus_stop(fifth, forth, third, second, first):
	bus_stop = fifth * 10000 + forth * 1000 + third * 100 + second * 10 + first
	bus_stop = TFL.lookup_bus_stop(bus_stop_name)
	msg = render_template("configure_bus_stop", bus_stop_name = bus_stop[1])

	return question(msg).repromt("I didn't get that. Can you repest the bus stop number clearly again?")



@ask.intent("CommingIntent")
def arrivals():

    busstop = "490012651S"

    arrivals = TFL.arrivals(busstop)
    arrivals = [ "#{} in {}minutes".format(i[0], math.floor(i[1]/60)) for i in arrivals ]
    msg = render_template('arrivals', arrivals=arrivals)

    return statement(msg)


@ask.intent("YesIntent")
def next_round():

    numbers = [randint(0, 9) for _ in range(3)]

    round_msg = render_template('round', numbers=numbers)

    session.attributes['numbers'] = numbers[::-1]  # reverse

    return question(round_msg)


@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})
def answer(first, second, third):
    winning_numbers = session.attributes.get('numbers', [1,2,3])
    if [first, second, third] == winning_numbers:
        msg = render_template('win')
    else:
        msg = render_template('lose')
    return statement(msg)

@ask.session_ended
def session_ended():
    return "Don't be late", 200

@app.teardown_request
def teardown_request(exception=None):
    print('this runs after request ')
    print(session.user)
    state = State(session)
    print("Current state is {}".format(state.load_user_data()))

#    print("after state {}".format(session.state))

@app.before_request
def before_request():
    print('this runs before request ')
    print(session.user)
    session.state = (session.state or 0) + 1


if __name__ == '__main__':

    app.run(debug=True)
from src.entities import SINGLE_SHOT, SEMI_AUTO, FULL_AUTO


def input_string(prompt):
    string_ = str(raw_input(prompt))
    return string_


def ask_user(prompt):
    yn_prompt = prompt + ' (y/n)'
    input_ = input_string(yn_prompt)
    result = input_.lower() == 'y'
    return result


def get_input(event, key, prompt, default, number=False):
    user_input = input_string(prompt)
    if user_input == '':
        user_input = default
    if number is True:
        user_input = int(user_input)
    event[key] = user_input
    return event


def build_attack_event():
    event = {}
    get_input(event=event,
              key='attacker',
              prompt='Specify attacker: ',
              default='dummy')
    get_input(event=event,
              key='target',
              prompt='Specify target: ',
              default='dummy')
    get_input(event=event,
              key='weapon',
              prompt='Specify weapon: ',
              default='dummy')
    get_input(event=event,
              key='roll_target',
              prompt='Specify roll target: ',
              default=100,
              number=True)
    get_input(event=event,
              key='num_attacks',
              prompt='Specify num attacks: ',
              default=1,
              number=True)
    get_input(event=event,
              key='firemode',
              prompt='Specify firemode (1/2/3): ',
              default=1,
              number=True)
    event['firemode'] = translate_firemode(event['firemode'])
    return event


def translate_firemode(input_number):
    if input_number == 1:
        firemode = SINGLE_SHOT
    elif input_number == 2:
        firemode = SEMI_AUTO
    elif input_number == 3:
        firemode = FULL_AUTO
    return firemode

from src.entities import SINGLE_SHOT


def input_string(prompt):
    string_ = str(raw_input(prompt))
    return string_


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
              default='NO_ATTACKER')
    get_input(event=event,
              key='target',
              prompt='Specify target: ',
              default='NO_TARGET')
    get_input(event=event,
              key='weapon',
              prompt='Specify weapon: ',
              default='NO_WEAPON')
    get_input(event=event,
              key='roll_target',
              prompt='Specify roll target: ',
              default=0,
              number=True)
    get_input(event=event,
              key='num_attacks',
              prompt='Specify num attacks: ',
              default=1,
              number=True)
    get_input(event=event,
              key='firemode',
              prompt='Specify firemode: ',
              default=SINGLE_SHOT)
    return event

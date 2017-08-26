import json

from src.action.action import Action
from src.entities.character import get_char
from src.entities.weapon import get_weapon
from src.util.string_util import convert_to_snake_case


ENEMY_ROLL = 'enemy_roll'
ALLY_ROLL = 'ally_roll'
ALLIES = 'allies'
ENEMIES = 'enemies'
TABLE_NAME = 'name'
DIAZ_INFECTED = False
BRO = 'pc_present'

TABLES = {
    'heth': {ALLIES: 22,
             ENEMIES: 12,
             TABLE_NAME: 'heth',
             ENEMY_ROLL: 65,
             ALLY_ROLL: 39},
    'caele': {ALLIES: 14,
              ENEMIES: 8,
              TABLE_NAME: 'caele',
              ENEMY_ROLL: 65,
              ALLY_ROLL: 55},
    'priest': {ALLIES: 7,
               ENEMIES: 4,
               TABLE_NAME: 'priest',
               ENEMY_ROLL: 65,
               ALLY_ROLL: 45},
    'diaz': {ALLIES: 14,
             ENEMIES: 6,
             TABLE_NAME: 'diaz',
             ENEMY_ROLL: 55,
             ALLY_ROLL: 40}
}


def heyo():
    input_ = None
    while input_ != 'quit':
        try:
            input_ = raw_input('Input stuff: ')
            if input_ == 'run':
                module_run()
            if input_ == 'attack':
                module_attack()
            if input_ == 'info':
                module_info()
            if input_ == 'kill':
                module_kill()
            if input_ == 'allies':
                module_add_allies()
        except Exception as error:
            print 'DISASTER.'
            print error


def get_number(prompt):
    number = int(raw_input(prompt))
    return number


def select_table():
    table_name = raw_input('Specify table: ')
    table = TABLES[table_name]
    return table, table_name


def module_add_allies():
    table, table_name = select_table()
    num_allies = get_number('How many allies?: ')
    table[ALLIES] = table[ALLIES] + num_allies
    TABLES[table_name] = table


def module_modify_enemies():
    table, table_name = select_table()
    num_enemies = get_number('How many enemies?: ')
    table[ENEMIES] = table[ENEMIES] + num_enemies
    TABLES[table_name] = table


def module_kill():
    table, table_name = select_table()
    table[ENEMIES] = table[ENEMIES] - 1
    TABLES[table_name] = table


def module_info():
    for table in TABLES.values():
        print '[%s]' % table[TABLE_NAME]
        print 'Allies: %s, Enemies: %s' % (table[ALLIES], table[ENEMIES])


def module_attack():
    print '_____________[NEW ATTACK]_____________'
    try:
        input_ = raw_input('Genestealers attack who?: ')
        num_attacks = int(raw_input('How many attacks?: '))
        roll_target = int(raw_input('Roll target?: '))
        target_name = convert_to_snake_case(input_)
        genestealer = get_char('auran_genestealer')
        weapon = get_weapon('rending_claws')
        target = get_char(target_name)
        for _ in range(num_attacks):
            attack = genestealer.melee_attack(weapon, target)
            attack.try_action(roll_target)
            if attack.is_successfull():
                for hit in attack.hits_generator():
                    target.mitigate_hit(attack, hit)
    except Exception:
        print 'Something broke. Oops.'


def module_run():
    input_ = raw_input(
        'Run module: which table? (heth, caele, priest, diaz or all) ')
    if input_ == 'all':
        for table in TABLES:
            simulate_round(table)
    else:
        for table in TABLES:
            if input_ == table[TABLE_NAME]:
                simulate_round(table)


def simulate_round(table):
    table_name = table[TABLE_NAME]
    if table.get('done') is not True:
        if table_name == 'diaz':
            if DIAZ_INFECTED is False:
                diaz_infection_roll()
            else:
                print 'Diaz already infected.'
        enemy_dos = max(get_dos(table[ENEMY_ROLL]), 0)
        ally_dos = max(get_dos(table[ALLY_ROLL]), 0)
        allies = max(table[ALLIES] - enemy_dos, 0)
        enemies = max(table[ENEMIES] - ally_dos, 0)
        print '[%s]' % table_name
        print '%s allies die in group %s. %s allies remain.' % (enemy_dos, table_name, allies)
        print '%s enemies die in group %s. %s enemies remain.' % (ally_dos, table_name, enemies)
        table[ALLIES] = allies
        table[ENEMIES] = enemies
        if enemies == 0 or allies == 0:
            print 'Fight is over.'
            table['done'] = True


def diaz_infection_roll():
    diaz_dodge_dos = get_dos(44)
    gs_ws_dos = get_dos(55)
    if gs_ws_dos >= diaz_dodge_dos:
        print 'DIAZ DID NOT DODGE.'
        diaz_toughness = Action()
        diaz_toughness.try_action(41)
        if diaz_toughness.is_successfull() is not True:
            global DIAZ_INFECTED
            DIAZ_INFECTED = True
            print 'DIAZ WAS INFECTED!'
        else:
            print 'Diaz bitten but not infected!'


def get_dos(roll_target):
    action = Action()
    action.try_action(roll_target)
    return action.get_degrees_of_success()

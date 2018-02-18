from src.dwca_log.log import get_log
from src.handler import build_base_attack
from src.modifiers.roll_modifier import add_roll_mod, PSY_RATING_MOD
from src.modifiers.states import Push, Fettered, Unfettered
from src.util.event_util import update_adhoc_dict
from src.util.user_input import try_user_choose_from_list


LOG = get_log(__name__)


def handler_pr_bonus(event):
    LOG.info('Choose power level: ')
    power_level = try_user_choose_from_list(
        [Push.name, Fettered.name, Unfettered.name])
    event = update_adhoc_dict(event, {power_level: True})

    attack = build_base_attack(event)
    psy_rating = attack.effective_psy_rating if attack.effective_psy_rating is not None else 0
    pr_bonus = psy_rating * 5
    LOG.info('+%s from effective psy rating. (%s)',
             pr_bonus, psy_rating)
    event = add_roll_mod(event, pr_bonus, PSY_RATING_MOD)
    return event

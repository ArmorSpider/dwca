from src.cli import ask_user
from src.entities import PENETRATION
from src.entities.char_stats import STAT_TGH
from src.message_queue import queue_message
from src.modifiers.modifier import Modifier


class RazorSharp(Modifier):

    name = 'razor_sharp'

    def modify_penetration(self, attack, current_pen):
        if attack.get_degrees_of_success() >= 2:
            weapons_penetration = attack.get_weapon_stat(PENETRATION)
            current_pen += weapons_penetration
            return current_pen
        else:
            return current_pen


class Tearing(Modifier):

    name = 'tearing'

    def modify_tearing_dice(self, attack, current_tearing_dice):
        return current_tearing_dice + 1


class Felling(Modifier):

    name = 'felling'


class Toxic(Modifier):

    name = 'toxic'

    @staticmethod
    def handle_toxic(attack, effective_damage):
        toxic_value = attack.get_weapon().get_quality(Toxic.name)
        if toxic_value is not None and effective_damage > 0:
            penalty = 5 * effective_damage
            queue_message('TOXIC: %s should roll %s -%s or take %s true damage.' %
                          (attack.get_target(), STAT_TGH, penalty, toxic_value))


class TwinLinked(Modifier):

    name = 'twin_linked'

    def modify_num_hits(self, attack, current_num_hits):
        if attack.get_degrees_of_success() >= 2:
            current_num_hits += 1
        return current_num_hits


class Accurate(Modifier):

    name = 'accurate'

    def modify_num_dice(self, attack, current_num_dice):
        if attack.get_degrees_of_success() >= 2:
            if ask_user('Was attack aimed?') is True:
                current_num_dice += 1
                if attack.get_degrees_of_success() >= 4:
                    current_num_dice += 1
        return current_num_dice


class Blast(Modifier):

    name = 'blast'

    def modify_num_hits(self, attack, current_num_hits):
        if attack.get_target().is_horde():
            blast_value = attack.get_weapon().get_quality(self.name)
            bonus_hits = max(1, blast_value - 1)
            current_num_hits += bonus_hits
        return current_num_hits


class PowerField(Modifier):

    name = 'power_field'

    def modify_num_hits(self, attack, current_num_hits):
        if attack.get_target().is_horde():
            current_num_hits += 1
        return current_num_hits


class Storm(Modifier):

    name = 'storm'


class Devastating(Modifier):

    name = 'devastating'

from src.dwca_log.log import get_log
from src.entities.character import Character


LOG = get_log(__name__)


class Vehicle(Character):

    def is_vehicle(self):
        return True

    def get_modded_toughness_bonus(self, attack, hit_location):
        return 0

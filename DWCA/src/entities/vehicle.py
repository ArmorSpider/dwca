from src.dwca_log.log import get_log
from src.entities import HALF_MOVE, FULL_MOVE, CHARGE_MOVE, RUN_MOVE
from src.entities.character import Character


LOG = get_log(__name__)


class Vehicle(Character):

    def is_vehicle(self):
        return True

    def get_modded_toughness_bonus(self, attack, hit_location):
        return 0

    @property
    def movement(self):
        move_mod = self.tactical_speed
        half_move = move_mod
        full_move = move_mod * 2
        charge_move = move_mod * 2
        run_move = move_mod * 2
        movement = {HALF_MOVE: half_move,
                    FULL_MOVE: full_move,
                    CHARGE_MOVE: charge_move,
                    RUN_MOVE: run_move}
        return movement

    @property
    def tactical_speed(self):
        speed = self.get_stat('speed', 0)
        return speed

from enum import Enum
import requests
import json
from utils.map_convert import Map

from data.CONSTANTS import *


with open("data/dofusmap_hint.json") as f:
    hint_names = json.load(f)

class HintType(Enum):
    POI = "poi"
    NPC = "npc"

class HintDirection(Enum):
    RIGHT = "right"
    LEFT = "left"
    TOP = "top"
    BOTTOM = "bottom"

    @staticmethod
    def direction_converter(direction: str,):
        directions = {
            0: HintDirection.RIGHT,
            2: HintDirection.BOTTOM,
            4: HintDirection.LEFT,
            6: HintDirection.TOP,
        }
        return directions.get(direction)

class Hint:
    hint_type = None
    predicted_pos = None
    hint_label = None
    hint_direction = None
    base_id = None


    def __init__(self, type, id, direction, origin_map):
        self.hint_type = type
        self.hint_direction = HintDirection.direction_converter(direction)
        self.base_id = id
        self.origin_map = origin_map
        self.get_label()
        self.get_position()


    def get_label(self):
        if self.hint_label is not None:
            return self.hint_label
        res = requests.get(f"{POI_BASE}{self.hint_type.value}/{self.base_id}").json()
        self.hint_label = res.get("label")
        return self.hint_label

    def get_position(self):
        if self.hint_type == HintType.NPC:
            return None
        if self.predicted_pos is not None:
            return self.predicted_pos
        res = requests.get(
            DOFUS_MAP_HUNT,
            params={
                "x": self.origin_map.x,
                "y": self.origin_map.y,
                "direction": self.hint_direction.value,
                "world": 0,
                "language": "fr"
            }
        ).json()
        for hint in res.get('hints', []):
            hint_name = hint_names[str(hint.get("n"))]
            if hint_name == self.get_label():
                self.predicted_pos = Map(None, hint.get("x"), hint.get("y"))

        if self.predicted_pos is None:
            print(f"Started in {self.origin_map}, direction {self.hint_direction.value}\n")
            print(f"Couldnt find {self.get_label()} in {[hint_names[str(hint.get('n'))] for hint in res.get('hints', [])]}")
        return self.predicted_pos
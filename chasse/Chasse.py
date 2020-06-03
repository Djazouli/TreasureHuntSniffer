import time
from chasse.Hint import Hint, HintType

class Chasse():
    start_time = None
    starting_map = None
    next_hint = None
    etapes = []

    def __init__(self, starting_map, current_map, current_steps):
        self.start_time = time.time()
        self.starting_map = starting_map
        count = 0
        for step in current_steps:
            type = HintType.POI if step.get("__type__") == 'TreasureHuntStepFollowDirectionToPOI' else HintType.NPC
            id = step.get("poiLabelId") if type == HintType.POI else step.get("npcId")
            hint = Hint(type, id, step.get("direction"), current_map if count else starting_map)
            self.etapes.append(hint)
        self.next_hint = self.etapes[-1]

    def add_step(self, current_map, step):
        type = HintType.POI if step.get("__type__") == 'TreasureHuntStepFollowDirectionToPOI' else HintType.NPC
        id = step.get("poiLabelId") if type == HintType.POI else step.get("npcId")
        hint = Hint(type, id, step.get("direction"), current_map)
        self.etapes.append(hint)
        self.next_hint = hint
        return

    def end(self):
        return time.time() - self.start_time
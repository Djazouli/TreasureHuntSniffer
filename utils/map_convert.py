import json

class Mapper():
    def __init__(self):
        with open("data/MapPositions.json") as f:
            self.base_map = json.load(f)
        self._id2pos = {}

        for map in self.base_map:
            self._id2pos[map["id"]] = {
                "x": map["posX"],
                "y": map["posY"],
            }


    def id2pos(self, map_id):
        return Map(map_id, **self._id2pos.get(map_id))

class Map():
    def __init__(self, id, x ,y):
        self.id = id
        self.x = x
        self.y = y

    def __str__(self):
        return f"[{self.x}, {self.y}]"
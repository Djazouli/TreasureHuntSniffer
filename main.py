import pyshark
import logging

from utils.map_convert import Mapper
from chasse.Chasse import Chasse
from chasse.Hint import HintType
from labot.sniffer.network import launch_in_thread

logging.basicConfig(level=logging.FATAL)

logger = logging.getLogger("main")

capture = pyshark.LiveCapture(interface="en7", bpf_filter='tcp port 5555 and len > 66')


def log_message(msg):
    logger.info(msg)

map = Mapper()
current_map = None
chasse = None

test_reminder = None



def manage_message(msg):
    global map
    global current_map
    global test_reminder
    global chasse
    msg = msg.json()
    if msg["__type__"] in {"ChatServerMessage", "ChatServerWithObjectMessage", "GameMapMovementMessage"}:
        return
    log_message(msg)

    if msg["__type__"] == "CurrentMapMessage":
        current_map = map.id2pos(msg['mapId'])
        return
    elif msg["__type__"] == "MapComplementaryInformationsDataMessage":
        # look for phorreur
        for actor in msg.get("actors", []):
            if actor.get("__type__") == "GameRolePlayTreasureHintInformations" and chasse is not None and chasse.next_hint.base_id == actor.get('npcId'):
                print(f"Found phorreur in {current_map}")
    elif msg["__type__"] == "TreasureHuntMessage":
        if len(msg["knownStepsList"]) == 1 and msg['knownStepsList'][0].get('__type__') == 'TreasureHuntStepFight':
            print("Fighting time!")
            return
        if chasse is None:
            chasse = Chasse(map.id2pos(msg['startMapId']), current_map, msg["knownStepsList"])
        else:
            if len(msg["knownStepsList"]) == test_reminder:
                return
            chasse.add_step(current_map, msg["knownStepsList"][-1])
            test_reminder = len(msg["knownStepsList"])
        if chasse.next_hint.hint_type == HintType.NPC:
            print("Next hint is a phorreur, I'll tell you when we get there.")
        else:
            print(f"You have to aim towards {chasse.next_hint.get_position()}")

    elif msg["__type__"] == "TreasureHuntFinishedMessage" and chasse is not None:
        print(f"Took {chasse.end()} seconds")
        chasse = None

    # Number of chest may be in TreasureHuntDigRequestAnswerMessage, key "result"


launch_in_thread(manage_message)
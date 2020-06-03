import pyshark
import logging


from decoder.PacketParser import PacketParser
from utils.map_convert import Mapper
from chasse.Chasse import Chasse
from chasse.Hint import HintType

logging.basicConfig(level=logging.FATAL)

logger = logging.getLogger("main")

capture = pyshark.LiveCapture(interface="en7", bpf_filter='tcp port 5555 and len > 66')


def log_message(msg, from_client):
    if from_client:
        logger.info("Paquet Dofus Envoyé")
    else:
        logger.info("Paquet Dofus Reçu")
    logger.info(msg)

map = Mapper()
parser = PacketParser()
current_map = None
chasse = None

test_reminder = None

for packet in capture.sniff_continuously():
    from_client, msg = parser.parse_packet(packet)
    if msg is None:
        continue

    if msg["__type__"] in {"ChatServerMessage", "ChatServerWithObjectMessage", "GameMapMovementMessage"}:
        continue
    log_message(msg, from_client)

    if msg["__type__"] == "CurrentMapMessage":
        current_map = map.id2pos(msg['mapId'])
        continue
    if msg["__type__"] == "MapComplementaryInformationsDataMessage":
        # look for phorreur
        for actor in msg.get("actors", []):
            if actor.get("__type__") == "GameRolePlayTreasureHintInformations" and chasse is not None and chasse.next_hint.base_id == actor.get('npcId'):
                print(f"Found phorreur in {current_map}")
        pass
    if msg["__type__"] == "TreasureHuntMessage":
        if len(msg["knownStepsList"]) == 1 and msg['knownStepsList'][0].get('__type__') == 'TreasureHuntStepFight':
            print("Fighting time!")
            continue
        if chasse is None:
            chasse = Chasse(map.id2pos(msg['startMapId']), current_map, msg["knownStepsList"])
        else:
            if len(msg["knownStepsList"]) == test_reminder:
                continue
            chasse.add_step(current_map, msg["knownStepsList"][-1])
            test_reminder = len(msg["knownStepsList"])
        if chasse.next_hint.hint_type == HintType.NPC:
            print("Next hint is a phorreur, I'll tell you when we get there.")
        else:
            print(f"You have to aim towards {chasse.next_hint.get_position()}")
    if msg["__type__"] == "GameFightEndMessage" and chasse is not None:
        print(f"Took {chasse.end()} seconds")
        chasse = None



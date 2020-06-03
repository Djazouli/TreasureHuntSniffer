import socket
import logging
from decoder import decoder

HOST = socket.gethostbyname(socket.gethostname())
logger = logging.getLogger("PacketParser")


class PacketParser():
    def __init__(self):
        self.waiting_data = []
        return

    def parse_packet(self, packet):
        from_client = packet.ip.src == HOST
        self.waiting_data = []
        try:
            data = packet.data.data
        except AttributeError:
            logger.info(f"Packet failed: {packet}")
            return from_client, None
        self.waiting_data.append(data)
        try:
            msg = decoder.readMsg(''.join(self.waiting_data), from_client)
        except Exception:
            logger.info(f"Failed to parse message")
            msg = None
        if msg is None:
            logger.info("Found incomplete message")
            return from_client, None
        self.waiting_data = []
        return (from_client, msg,)
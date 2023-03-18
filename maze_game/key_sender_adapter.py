from bs import KeySender, ecodes as e
from typing import List
from .typing import MoveEnum


MOVE_TO_KEYS = {
    MoveEnum.UP: e.KEY_UP,
    MoveEnum.DOWN: e.KEY_DOWN,
    MoveEnum.LEFT: e.KEY_LEFT,
    MoveEnum.RIGHT: e.KEY_RIGHT,
}


class KeySenderAdapter:

    def __init__(self, sender: KeySender):
        self._sender = sender

    def send_many(self, moves: List[MoveEnum]):
        self._sender.send_many([MOVE_TO_KEYS[m] for m in moves])

import hashlib

from server_impl.server_config import ckv
from game_server_core import GameServerCore


def get_server_core(controller):
    key = ckv.get_ckv_game_server_core()
    game_core = controller.mem_cache.get(key)
    if game_core is None:
        game_core = GameServerCore()
        controller.mem_cache.set(key, game_core)
    return game_core


def get_md5_str(msg):
    md5 = hashlib.md5()
    md5.update(msg)
    return md5.hexdigest()
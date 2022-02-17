from pokemon_showdown_rl.battle_context import BattleContext
from pokemon_showdown_rl.showdown.parse_msg import parse_player

class Room:
    def __init__(self, room_id, username, logger):
        self.room_id = room_id
        self.logger = logger
        self.context = BattleContext(username, self.logger)

    async def handle_msg(self, websocket, msg_type, msg_data, tags):
        if msg_type == 'title':
            self.context.battle.apply_title(msg_data)
        elif msg_type == 'request':
            self.context.apply_request(msg_data)
        elif msg_type == 'gametype':
            self.context.battle.apply_gametype(msg_type)
        elif msg_type == 'player':
            self.context.apply_player(msg_data)
        elif msg_type == 'teamsize':
            self.context.battle.apply_teamsize(msg_data)
        elif msg_type == 'gen':
            self.context.battle.apply_gen(msg_data)
        elif msg_type == 'tier':
            self.context.battle.apply_tier(msg_data)
        elif msg_type == 'rule':
            self.context.battle.apply_rule(msg_data)
        elif msg_type == 'turn':
            # Look at request and validate/update game state
            # TODO: choose an action
            await websocket.send(f'{self.room_id}|/choose default')
        elif msg_type == 'win':
            # Do something to indicate the game is over
            pass
        elif msg_type == 'move':
            self.context.battle.apply_move(msg_data)
        elif msg_type == 'switch':
            self.context.battle.apply_switch(msg_data)
        elif msg_type == 'drag':
            self.context.battle.apply_drag(msg_data)
        elif msg_type == 'detailschange':
            self.context.battle.apply_detailschange(msg_data)
        elif msg_type == 'replace':
            self.context.battle.apply_replace(msg_data)
        elif msg_type == 'swap':
            self.context.battle.apply_swap(msg_data)
        elif msg_type == 'cant':
            pass
        elif msg_type == 'faint':
            self.context.battle.apply_faint(msg_data)
            # Look at request and validate/update game state
            # TODO: choose a new pokemon to switch to
            await websocket.send(f'{self.room_id}|/choose default')
        elif msg_type == 'error':
            # TODO: handle error
            pass
        elif msg_type == '-formechange':
            self.context.battle.apply_formechange(msg_data)
        elif msg_type == '-block':
            pass
        elif msg_type == '-notarget':
            pass
        elif msg_type == '-miss':
            pass
        elif msg_type == '-damage':
            self.context.battle.apply_damage(msg_data)
        elif msg_type == '-heal':
            self.context.battle.apply_heal(msg_data)
        elif msg_type == '-sethp':
            self.context.battle.apply_sethp(msg_data)
        elif msg_type == '-status':
            self.context.battle.apply_status(msg_data)
        elif msg_type == '-curestatus':
            self.context.battle.apply_curestatus(msg_data)
        elif msg_type == '-cureteam':
            self.context.battle.apply_cureteam(msg_data)
        elif msg_type == '-boost':
            self.context.battle.apply_boost(msg_data)
        elif msg_type == '-unboost':
            self.context.battle.apply_unboost(msg_data)
        elif msg_type == '-setboost':
            self.context.battle.apply_setboost(msg_data)
        elif msg_type == '-swapboost':
            self.context.battle.apply_swapboost(msg_data)
        elif msg_type == '-invertboost':
            self.context.battle.apply_invertboost(msg_data)
        elif msg_type == '-clearboost':
            self.context.battle.apply_clearboost(msg_data)
        elif msg_type == '-clearallboost':
            self.context.battle.apply_clearallboost()
        elif msg_type == '-clearpositiveboost':
            self.context.battle.apply_clearpositiveboost(msg_data)
        elif msg_type == '-clearnegativeboost':
            self.context.battle.apply_clearnegativeboost(msg_data)
        elif msg_type == '-copyboost':
            self.context.battle.apply_copyboost(msg_data)
        elif msg_type == '-weather':
            self.context.battle.apply_weather(msg_data)
        elif msg_type == '-fieldstart':
            self.context.battle.apply_fieldstart(msg_data)
        elif msg_type == '-fieldend':
            self.context.battle.apply_fieldend(msg_data)
        elif msg_type == '-sidestart':
            self.context.battle.apply_sidestart(msg_data)
        elif msg_type == '-sideend':
            self.context.battle.apply_sideend(msg_data)
        elif msg_type == '-start':
            self.context.battle.apply_start(msg_data)
        elif msg_type == '-end':
            self.context.battle.apply_end(msg_data)
        elif msg_type == '-crit':
            pass
        elif msg_type == '-supereffective':
            # TODO: find a way to have this represented/stored
            # so it can be used to increase reward
            pass
        elif msg_type == '-resisted':
            # TODO: find a way to have this represented/stored
            # so it can be used to decrease reward
            pass
        elif msg_type == '-immune':
            # TODO: find a way to have this represented/stored
            # so it can be used to decrease reward
            pass
        elif msg_type == '-item':
            self.context.battle.apply_item(msg_data)
        elif msg_type == '-enditem':
            self.context.battle.apply_enditem(msg_data)
        elif msg_type == '-ability':
            pass
        elif msg_type == '-endability':
            pass
        elif msg_type == '-transform':
            pass
        elif msg_type == '-mega':
            pass
        elif msg_type == '-primal':
            pass
        elif msg_type == '-burst':
            pass
        elif msg_type == '-zpower':
            pass
        elif msg_type == '-zbroken':
            pass
        elif msg_type == '-activate':
            pass
        elif msg_type == '-hint':
            pass
        elif msg_type == '-center':
            pass
        elif msg_type == '-message':
            pass
        elif msg_type == '-combine':
            pass
        elif msg_type == '-waiting':
            pass
        elif msg_type == '-prepare':
            pass
        elif msg_type == '-mustrecharge':
            pass
        elif msg_type == '-hitcount':
            pass
        elif msg_type == '-singlemove':
            pass
        elif msg_type == '-singleturn':
            pass
        elif msg_type == '':
            # Ignore chat spacer messages
            pass
        else:
            self.logger.info(
                f'INFO | Unhandled message type, {msg_type}, with data, {msg_data}'
            )

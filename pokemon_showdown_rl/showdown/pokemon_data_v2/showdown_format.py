from dataclasses import dataclass


@dataclass
class ShowdownFormat:
    name: str
    mod: str
    section: str
    description: str
    game_type: str
    team: str
    ruleset: list[str]
    banlist: list[str]
    unbanlist: list[str]
    restricted: list[str]


    @staticmethod
    def from_json(json_data):
        return ShowdownFormat(
            json_data['name'],
            json_data['mod'],
            json_data['section'],
            json_data['desc'],
            json_data['game_type'],
            json_data['team'],
            json_data['ruleset'],
            json_data['banlist'],
            json_data['unbanlist'],
            json_data['restricted']
        )

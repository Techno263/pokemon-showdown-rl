from dataclasses import dataclass

@dataclass
class ItemEntry:
    name: str
    pokemon: list[str]

    @staticmethod
    def from_json(json_data):
        return ItemEntry(json_data['name'], json_data['pokemon'])

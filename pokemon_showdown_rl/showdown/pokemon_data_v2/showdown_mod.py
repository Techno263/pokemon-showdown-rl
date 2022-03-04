from dataclasses import dataclass

@dataclass
class ShowdownMod:
    tiers: dict[str, str]
    items: dict[str, str]
    override_tier: dict[str, str]

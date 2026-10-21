"""
Bodo Cultural Heritage, Festivals, Bathou Tradition, Attire, Instruments, and Clans Treasury.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from bodonlp.constants import BODO_CLANS, SEASONS, BODO_MONTHS, DAYS_OF_WEEK


@dataclass
class Festival:
    name: str
    bodo_name: str
    roman: str
    timing: str
    significance: str
    rituals: List[str]


@dataclass
class Instrument:
    name: str
    bodo_name: str
    roman: str
    instrument_type: str
    materials: str
    cultural_use: str


@dataclass
class Attire:
    name: str
    bodo_name: str
    roman: str
    gender: str
    description: str
    motifs: List[str]


FESTIVALS: List[Festival] = [
    Festival(
        name="Bwisagu",
        bodo_name="बैसागु",
        roman="Bwisagu",
        timing="Mid-April (Month of Bwisakh / First week of Assamese Bohag)",
        significance="The most cherished spring New Year festival of the Bodos, celebrating nature's renewal, agriculture, and youth harmony.",
        rituals=[
            "Makhau (Cattle worship on first day, washing cows in the river and feeding them turmeric and brinjals)",
            "Mansi Bwisagu (Human day, seeking blessings from elders and donning new handwoven clothes)",
            "Bwisagu Mwsanai (Spirited Bwisagu dance with Sifung, Kham, and Serja)",
            "Serving traditional Zou (rice brew) and Oma Bedor (pork dishes) to guests"
        ]
    ),
    Festival(
        name="Domashi",
        bodo_name="दोमासि",
        roman="Domashi",
        timing="Mid-January (Month of Magh / Winter solstice)",
        significance="Harvest festival of joy and thanksgiving for abundant granaries, coinciding with Magh Bihu.",
        rituals=[
            "Erection of Bhelaghar and Meji tall conical straw structures in paddy fields",
            "Lighting the ceremonial dawn bonfire to pray for prosperity",
            "Community feasting with traditional pithas (rice cakes) and curd",
            "Traditional sports: egg fighting and wrestling"
        ]
    ),
    Festival(
        name="Kherai",
        bodo_name="खेराइ",
        roman="Kherai",
        timing="Autumn / Winter or post-transplantation",
        significance="Grand community sacrificial prayer to Bathoubwrai (Supreme Creator) for village protection, good crops, and peace.",
        rituals=[
            "Doudini (shamanic female dancer) in trance executing 18 sacred ritual dances",
            "Deuri and Oja chanting sacred Bodo hymns around the Bathou altar",
            "Enthronement of the holy Sijou tree adorned with five rings of split bamboo"
        ]
    ),
    Festival(
        name="Garja",
        bodo_name="गार्जा",
        roman="Garja",
        timing="End of Bwisagu or monsoon entry",
        significance="Village sanctification rite to ward off diseases, pests, evil spirits, and natural calamities.",
        rituals=[
            "Sealing the village perimeter to prevent entry during ritual chanting",
            "Purification of each household with basil water and sacred embers"
        ]
    ),
    Festival(
        name="Katrigasa",
        bodo_name="खाथ्रिगासा",
        roman="Katrigasa",
        timing="Autumn (Month of Khati / October)",
        significance="Festival of lights dedicated to blooming paddy plants in the fields.",
        rituals=[
            "Lighting earthen lamps (gasa) in paddy fields, cowsheds, and granaries",
            "Praying for pest-free paddy stalks to ensure abundant winter harvest"
        ]
    )
]

INSTRUMENTS: List[Instrument] = [
    Instrument(
        name="Sifung",
        bodo_name="सिफुं",
        roman="Sifung",
        instrument_type="Aerophone (Transverse Bamboo Flute)",
        materials="Long hollow bamboo node with 5 finger holes (unique to Bodo music)",
        cultural_use="The soul of Bodo melodies, producing poignant haunting notes in Bwisagu dance and Bathou devotion."
    ),
    Instrument(
        name="Kham",
        bodo_name="खाम",
        roman="Kham",
        instrument_type="Membranophone (Double-headed Barrel Drum)",
        materials="Hollowed wood trunk with goat/cow skin drumheads tightened by leather thongs",
        cultural_use="Provides the rhythmic heartbeat for Kherai and Bwisagu folk dances."
    ),
    Instrument(
        name="Serja",
        bodo_name="सेर्जा",
        roman="Serja",
        instrument_type="Chordophone (Bowed 4-string Violin)",
        materials="Wood resonator bowl covered with monitor lizard skin or thin timber, horsehair bow",
        cultural_use="Plays melancholic romantic tunes and accompaniment for wandering bard songs."
    ),
    Instrument(
        name="Tharkha",
        bodo_name="थारखा",
        roman="Tharkha",
        instrument_type="Idiophone (Split Bamboo Clapper)",
        materials="Split mature bamboo stalk",
        cultural_use="Keeps sharp tempo and syncopated cadence during group celebrations."
    ),
    Instrument(
        name="Jotha",
        bodo_name="जोथा",
        roman="Jotha",
        instrument_type="Idiophone (Bronze Hand Cymbals)",
        materials="Bell metal / bronze",
        cultural_use="Complements the Kham drum in temple Kherai rituals."
    ),
    Instrument(
        name="Gongwna",
        bodo_name="गंङना",
        roman="Gongwna",
        instrument_type="Lamellophone (Bamboo Jaw Harp)",
        materials="Meticulously carved thin vibrating bamboo tongue",
        cultural_use="Intimate instrument played by young maidens by plucking while held between teeth."
    )
]

ATTIRE: List[Attire] = [
    Attire(
        name="Dokhona",
        bodo_name="दखना",
        roman="Dokhona",
        gender="Female",
        description="Traditional graceful drape wrapped around the torso from above the chest down to the ankles.",
        motifs=["Pahar agor (mountain hills)", "Daorai agor (peacock feather)", "Hajw agor (mountain peaks)"]
    ),
    Attire(
        name="Aronai",
        bodo_name="आरोनाइ",
        roman="Aronai",
        gender="Unisex",
        description="The ultimate symbol of Bodo dignity and hospitality; a ceremonial scarf draped around the neck.",
        motifs=["Floral diamond patterns", "Phul agor", "Geometric borders in red, yellow, green"]
    ),
    Attire(
        name="Gamcha",
        bodo_name="गामसा",
        roman="Gamcha / Gamsa",
        gender="Male",
        description="Handwoven lower waist cloth tied around the waist, reaching below the knees.",
        motifs=["Checked patterns in saffron, maroon, and white"]
    ),
    Attire(
        name="Phasra",
        bodo_name="फासरा",
        roman="Phasra",
        gender="Female",
        description="Fine ceremonial upper wrapper scarf thrown elegantly across the shoulders over the Dokhona.",
        motifs=["Intricate golden end borders", "Traditional silkworm spun motifs"]
    )
]


def list_festivals() -> List[Festival]:
    """Return all traditional Bodo festivals."""
    return FESTIVALS


def get_festival(name: str) -> Optional[Festival]:
    """Look up a festival by English or Bodo name."""
    clean = name.lower().strip()
    for f in FESTIVALS:
        if clean in (f.name.lower(), f.bodo_name.lower(), f.roman.lower()):
            return f
    return None


def list_instruments() -> List[Instrument]:
    """Return all traditional Bodo musical instruments."""
    return INSTRUMENTS


def list_attire() -> List[Attire]:
    """Return traditional Bodo clothing and attire."""
    return ATTIRE


def list_clans() -> List[Dict[str, str]]:
    """Return all prominent Bodo clans and surnames with meanings."""
    return BODO_CLANS


def get_bathou_principles() -> Dict[str, Any]:
    """Return the theological foundations and sacred symbols of Bathouism."""
    return {
        "deity": "Bathoubwrai (The Supreme Ultimate Being)",
        "sacred_plant": "Sijou (Euphorbia neriifolia)",
        "five_bamboo_rings": [
            {"ring": 1, "principle": "Thu (Truth / सत)"},
            {"ring": 2, "principle": "Lhu (Knowledge / ज्ञान)"},
            {"ring": 3, "principle": "Hau (Karma / Work / कर्म)"},
            {"ring": 4, "principle": "Bao (Beauty / Love / प्रीति)"},
            {"ring": 5, "principle": "Zao (Compassion / दया)"}
        ],
        "five_elements": ["Earth (हा)", "Water (दै)", "Fire (अर)", "Air (बार)", "Ether/Sky (अख्रां)"]
    }

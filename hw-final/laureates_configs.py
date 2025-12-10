from json_dict_processing import process_dictionary_with_config
from prizes_configs import prize_processor
from utils import process_year


CONFIG_PERSON = {
    "id": (["id"], int),
    "name": ["knownName", "en"],
    "gender": ["gender"],
    "birth_year": (["birth", "date"], process_year),
    "country_birth": ["birth", "place", "country", "en"],
    "country_now": ["birth", "place", "countryNow", "en"],
    "prizes_relevant": (["nobelPrizes"], prize_processor),
}

CONFIG_ORG = {
    "id": (["id"], int),
    "name": ["orgName", "en"],
    "founded_year": (["founded", "date"], process_year),
    "country_founded": ["founded", "place", "country", "en"],
    "country_now": ["founded", "place", "countryNow", "en"],
    "prizes_relevant": (["nobelPrizes"], prize_processor),
}


def process_persons(laureate):
    """
    Сделать плоский словарь для человека-лауреата
    """
    return process_dictionary_with_config(laureate, CONFIG_PERSON)

def process_orgs(laureate):
    """
    Сделать плоский словарь для организации-лауреата
    """
    return process_dictionary_with_config(laureate, CONFIG_ORG)


# Базовые тесты
_person_stub = {
    "id": "1",
    "knownName": {"en": "Test"},
    "birth": {"date": "2000-01-01", "place": {"country": {"en": "AA"}, "countryNow": {"en": "BB"}}},
    "nobelPrizes": [],
}
_org_stub = {
    "id": "2",
    "orgName": {"en": "Org"},
    "founded": {"date": "1990-01-01", "place": {"country": {"en": "AA"}, "countryNow": {"en": "BB"}}},
    "nobelPrizes": [],
}
assert process_persons(_person_stub)["id"] == 1
assert process_orgs(_org_stub)["name"] == "Org"

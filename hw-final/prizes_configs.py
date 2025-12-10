from json_dict_processing import process_list_of_dicts_with_config
from utils import process_year


CONFIG_PRIZE = {
    "prize_amount": ["prizeAmount"],
    "prize_amount_adjusted": ["prizeAmountAdjusted"],
    "award_year": (["awardYear"], process_year),
    "category_en": ["category", "en"],
    "prize_status": ["prizeStatus"],
}


def prize_processor(prizes_list):
    """Вернуть список плоских словарей по призам."""
    return process_list_of_dicts_with_config(prizes_list, CONFIG_PRIZE)


# Базовые тесты
_prize_sample = [{
    "prizeAmount": 10,
    "prizeAmountAdjusted": 12,
    "awardYear": "2001",
    "category": {"en": "Physics"},
    "prizeStatus": "received",
}]
_processed = prize_processor(_prize_sample)[0]
assert _processed["prize_amount"] == 10

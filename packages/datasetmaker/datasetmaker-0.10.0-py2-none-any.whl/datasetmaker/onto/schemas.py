from cerberus import schema_registry
from datasetmaker.onto.manager import read_entity

_cache: dict = dict()


def _allow(name: str) -> list:
    return _cache.get(name, read_entity(name)[name].to_list())


schema_registry.add('country', {
    'country': {'type': 'string', 'allowed': _allow('country')},
    'name': {'type': 'string'},
    'iso3': {'type': 'string'},
    'iso2': {'type': 'string'},
    'un_state': {'type': 'boolean'},
    'region4': {'type': 'string', 'allowed': _allow('region4')},
    'region6': {'type': 'string', 'allowed': _allow('region6')},
    'alt_name': {'type': 'string'},
    'denonym': {'type': 'string'},
    'slug': {'type': 'string'},
    'landlocked': {'type': 'boolean'}
})

schema_registry.add('region4', {
    'region4': {'type': 'string', 'allowed': _allow('region4')},
    'name': {'type': 'string'},
    'slug': {'type': 'string'},
})

schema_registry.add('region6', {
    'region6': {'type': 'string', 'allowed': _allow('region6')},
    'name': {'type': 'string'},
    'slug': {'type': 'string'},
})

schema_registry.add('gender', {
    'gender': {'type': 'string', 'allowed': _allow('gender')},
    'name': {'type': 'string'},
    'slug': {'type': 'string'},
})

schema_registry.add('nobel_laureate', {
    'nobel_laureate': {'type': 'string'},
    'nobel_firstname': {'type': 'string'},
    'nobel_surname': {'type': 'string'},
    'nobel_born': {'type': 'string'},
    'gender': {'type': 'string', 'allowed': _allow('gender') + ['org']},
    'nobel_born_city': {'type': 'string'},
    'nobel_born_country': {'type': 'string', 'allowed': _allow('country'), 'empty': True, 'nullable': True},
    'nobel_died': {'type': 'string'},
    'nobel_died_country': {'type': 'string', 'allowed': _allow('country'), 'empty': True, 'nullable': True}
})

schema_registry.add('nobel_category', {
    'nobel_category': {'type': 'string', 'allowed': _allow('nobel_category')},
    'name': {'type': 'string'}
})

schema_registry.add('nobel_prize', {
    'nobel_prize': {'type': 'string'},
    'nobel_laureate': {'type': 'string'},
    'nobel_category': {'type': 'string', 'allowed': _allow('nobel_category')},
    'nobel_motivation': {'type': 'string'},
    'year': {'type': 'integer', 'min': 1901}
})

schema_registry.add('nobel_instance', {
    'nobel_instance': {'type': 'string'},
    'nobel_category': {'type': 'string', 'allowed': _allow('nobel_category')},
    'year': {'type': 'integer', 'min': 1901}
})

schema_registry.add('pollster', {
    'pollster': {'type': 'string'},
    'name': {'type': 'string'},
    'valforsk_pollster_link': {'type': 'string'},
    'valforsk_in_mama': {'type': 'boolean'},
    'valforsk_mode': {'type': 'string'},
})

schema_registry.add('party', {
    'party': {'type': 'string', 'allowed': _allow('party')},
    'name': {'type': 'string'},
    'abbr': {'type': 'string'},
    'country': {'type': 'string', 'allowed': _allow('country'), 'nullable': True, 'empty': True},
    'slug': {'type': 'string'},
})

schema_registry.add('unsc_sanctioned_entity', {
    'unsc_sanctioned_entity': {'type': 'string'},
    'unsc_versionnum': {'type': 'string'},
    'unsc_first_name': {'type': 'string'},
    'unsc_un_list_type': {'type': 'string'},
    'unsc_reference_number': {'type': 'string'},
    'unsc_listed_on': {'type': 'string'},
    'unsc_comments1': {'type': 'string'},
    'unsc_name_original_script': {'type': 'string'},
    'unsc_submitted_on': {'type': 'string'}
})

schema_registry.add('unsc_sanctioned_individual', {
    'unsc_sanctioned_individual': {'type': 'string'},
    'unsc_versionnum': {'type': 'string'},
    'unsc_first_name': {'type': 'string'},
    'unsc_second_name': {'type': 'string'},
    'unsc_third_name': {'type': 'string'},
    'unsc_un_list_type': {'type': 'string'},
    'unsc_reference_number': {'type': 'string'},
    'unsc_listed_on': {'type': 'string'},
    'unsc_comments1': {'type': 'string'},
    'unsc_name_original_script': {'type': 'string'},
    'unsc_fourth_name': {'type': 'string'},
    'gender': {'type': 'string', 'allowed': _allow('gender'), 'empty': True, 'nullable': True},
    'unsc_submitted_by': {'type': 'string'}
})

schema_registry.add('esv_expenditure', {
    'esv_expenditure': {'type': 'string'},
    'name': {'type': 'string'}
})

schema_registry.add('esv_allocation', {
    'esv_allocation': {'type': 'string'},
    'name': {'type': 'string'}
})

schema_registry.add('sipri_currency', {
    'sipri_currency': {'type': 'string'}
})

schema_registry.add('wikipedia_visa_requirement', {
    'wikipedia_visa_requirement': {'type': 'string'}
})

schema_registry.add('wikipedia_head_gov', {
    'wikipedia_head_gov': {'type': 'string'},
    'wikipedia_head_gov_title': {'type': 'string'},
})

schema_registry.add('wikipedia_head_state', {
    'wikipedia_head_state': {'type': 'string'},
    'wikipedia_head_state_title': {'type': 'string'}
})

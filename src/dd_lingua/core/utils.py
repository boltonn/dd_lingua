from enum import StrEnum

from lingua import IsoCode639_3

LinguaIso639_to_Langcode = {iso.lower(): langcode for iso, langcode in IsoCode639_3.__dict__.items() if len(iso) == 3}

LinguaSupportedISO639_3 = StrEnum("LinguaSupportedISO639_3", list(LinguaIso639_to_Langcode.keys()))


def map_iso639_to_langcode(iso639: LinguaSupportedISO639_3):
    return LinguaIso639_to_Langcode[iso639]


class LinguaSupportedISO15924(StrEnum):
    Arab = "Arab"
    Cyrl = "Cyrl"
    Deva = "Deva"
    Latn = "Latn"


DEFAULT_LANGUAGES = [
    LinguaSupportedISO639_3.eng,
    LinguaSupportedISO639_3.fra,
    LinguaSupportedISO639_3.jpn,
    LinguaSupportedISO639_3.kor,
    LinguaSupportedISO639_3.rus,
    LinguaSupportedISO639_3.spa,
    LinguaSupportedISO639_3.ukr,
    LinguaSupportedISO639_3.zho,
]

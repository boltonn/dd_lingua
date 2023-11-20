from enum import StrEnum

from lingua import IsoCode639_3


LinguaSupportedISO639_3 = StrEnum(
    'LinguaSupportedISO639_3',
    [iso.lower() for iso in IsoCode639_3.__dict__.keys() if len(iso)==3]
)

class LinguaSupportedISO15924(StrEnum):
    Arab = "Arab"
    Cyrl = "Cyrl"
    Deva = "Deva"
    Latn = "Latn"
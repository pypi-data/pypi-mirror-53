# from .oecd import OECD
# from .skolverket import SKVClient
# from .socialstyrelsen import SocialstyrelsenClient
# from .wikipedia import Wikipedia
from .esv import ESVClient
from .hdi import HDIClient
from .nobel import NobelClient
from .sipri import SIPRI
from .unsc import UNSC
from .valforsk import ValforskClient
from .worldbank import WorldBank


available = {
    # 'oecd': OECD,
    # 'skolverket': SKVClient,
    # 'socialstyrelsen': SocialstyrelsenClient,
    # 'wikipedia': Wikipedia,
    'esv': ESVClient,
    'hdi': HDIClient,
    'nobel': NobelClient,
    'sipri': SIPRI,
    'unsc': UNSC,
    'valforsk': ValforskClient,
    'worldbank': WorldBank,
}

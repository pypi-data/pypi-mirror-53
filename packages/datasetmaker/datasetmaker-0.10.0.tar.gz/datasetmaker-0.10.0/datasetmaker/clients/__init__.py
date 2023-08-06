# from .hdi import HDI
# from .oecd import OECD
# from .skolverket import SKVClient
# from .socialstyrelsen import SocialstyrelsenClient
# from .wikipedia import Wikipedia
from .worldbank import WorldBank
from .esv import ESVClient
from .nobel import NobelClient
from .sipri import SIPRI
from .unsc import UNSC
from .valforsk import ValforskClient


available = {
    # 'hdi': HDI,
    # 'oecd': OECD,
    # 'skolverket': SKVClient,
    # 'socialstyrelsen': SocialstyrelsenClient,
    # 'wikipedia': Wikipedia,
    'worldbank': WorldBank,
    'esv': ESVClient,
    'nobel': NobelClient,
    'sipri': SIPRI,
    'unsc': UNSC,
    'valforsk': ValforskClient
}

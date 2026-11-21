"""
Paket naloga_segmentacija
Implementacije funkcij za segmentacijo slik.
"""

from .binarna_segmentacija import binarna_segmentacija
from .segmentiraj_rumeno_barvo import segmentiraj_rumeno_barvo
from .pobarvaj_sivinsko import pobarvaj_sivinsko
from .odvzem_ozadja import odvzem_ozadja
from .stevilo_regij import stevilo_regij
from .sredisca_regij import sredisca_regij
from .izrezi_regije import izrezi_regije
from .detekcija_4_kotnikov import detekcija_4_kotnikov
from .detekcija_4_kotnikov_adaptivno import detekcija_4_kotnikov_adaptivno
from .detekcija_plus import detekcija_plus

__all__ = [
    "binarna_segmentacija",
    "segmentiraj_rumeno_barvo",
    "pobarvaj_sivinsko",
    "odvzem_ozadja",
    "stevilo_regij",
    "sredisca_regij",
    "izrezi_regije",
    "detekcija_4_kotnikov",
    "detekcija_4_kotnikov_adaptivno",
    "detekcija_plus"
]
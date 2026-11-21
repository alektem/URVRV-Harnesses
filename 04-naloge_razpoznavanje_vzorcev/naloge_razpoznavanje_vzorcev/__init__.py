"""
Paket naloge_razpoznavanje_vzorcev
Implementacije funkcij za razpoznavanje vzorcev.
"""

from .razpoznava_likov import (
    pripravi_razpoznavalnik, 
    nalozi_razpoznavalnik,
    napovej_razred
)
from .augmentacija_vzorcev import (
    prikazi_augmentiran_vzorec,
    nalozi_augmentiranega_razpoznavalnika
)
from .vizualiziraj_utezi import vizualiziraj_utezi
from .vrednotenje_razpoznave import (
    matrika_zmede,
    vrednoti_razpoznavo
)
from .detekcija_z_razpoznavalnikom import detektiraj_okna
from .ucenje_detektorja import (
    pripravi_detektor,
    nalozi_detektor,
    detektiraj
)
from .ucenje_resnet18_detektorja import (
    pripravi_resnet18_detektor,
    nalozi_resnet18_detektor
)
from .odstranjevanje_duplikatov import odpravi_duplikate
from .vrednotenje_detekcij import (
    ujemanje_detekcij,
    vrednoti_detekcije
)
from .detekcija_z_okvirji import (
    pripravi_detektor_okvirjev,
    nalozi_detektor_okvirjev
)

__all__ = [
    pripravi_razpoznavalnik, nalozi_razpoznavalnik, napovej_razred,
    prikazi_augmentiran_vzorec, nalozi_augmentiranega_razpoznavalnika,
    vizualiziraj_utezi,
    matrika_zmede, vrednoti_razpoznavo,
    detektiraj_okna,
    pripravi_detektor, nalozi_detektor, detektiraj,
    pripravi_resnet18_detektor, nalozi_resnet18_detektor,
    odpravi_duplikate,
    ujemanje_detekcij, vrednoti_detekcije,
    pripravi_detektor_okvirjev, nalozi_detektor_okvirjev
]
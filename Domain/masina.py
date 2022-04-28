from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class Masina(Entitate):
    """
    descriere masina
    """
    model: str
    anAchizitie: int
    nrKm: float
    inGarantie: str

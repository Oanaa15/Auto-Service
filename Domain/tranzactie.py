from dataclasses import dataclass
import datetime

from Domain.entitate import Entitate


@dataclass
class Tranzactie(Entitate):
    """
    descriere tranzactie
    """
    idMasina: str
    idCard: str
    sumaPiese: float
    manopera: float
    dataOra: datetime

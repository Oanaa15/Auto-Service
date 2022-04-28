from dataclasses import dataclass
import datetime

from Domain.entitate import Entitate


@dataclass
class CardClient(Entitate):
    """
    contine datele cardului
    """
    nume: str
    prenume: str
    cnp: str
    dataNastere: datetime
    dataInreg: datetime

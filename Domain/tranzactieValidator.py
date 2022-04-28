from Domain.tranzactie import Tranzactie
from datetime import datetime

from Domain.tranzactieError import TranzactieError


class TranzactieValidator:
    def valideaza(self, tranzactie: Tranzactie) -> any:
        try:
            datetime.strptime(tranzactie.dataOra, '%d.%m.%Y %H:%M')
        except ValueError:
            raise TranzactieError(
                "Formatul datei trebuie sa fie: DD.MM.YYYY H:M")

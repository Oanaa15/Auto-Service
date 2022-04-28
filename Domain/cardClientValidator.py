from datetime import datetime
from Domain.cardClient import CardClient
from Domain.cardClientError import CardClientError


class CardClientValidator:
    def valideaza(self, cardClient: CardClient) -> any:
        if cardClient.cnp.isdigit() is False:
            raise CardClientError("CNP-ul trebuie sa contina cifre! ")
        try:
            datetime.strptime(cardClient.dataNastere, '%d.%m.%Y')
            datetime.strptime(cardClient.dataInreg, '%d.%m.%Y')
        except ValueError:
            raise CardClientError("Formatul datei trebuie sa fie: DD.MM.YYYY")

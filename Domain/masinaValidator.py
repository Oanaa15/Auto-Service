from Domain.masina import Masina
from Domain.masinaError import MasinaError


class MasinaValidator:
    def valideaza(self, masina: Masina) -> any:
        erori = []
        if masina.nrKm < 0:
            erori.append("Nr. de km trebuie sa fie pozitiv! ")
        if masina.anAchizitie < 0:
            erori.append("Anul achizitiei trebuie sa fie pozitiv! ")
        if len(erori) > 0:
            raise MasinaError(erori)

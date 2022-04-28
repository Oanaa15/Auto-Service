from Domain.entitate import Entitate
from Repository.repository import Repository


class RepositoryInMemory(Repository):
    def __init__(self):
        """
        creaza un repository in memory
        """
        self.entitati = {}

    def read(self, idEntitate=None) -> list | None:
        """
        da lista de entitati sau None daca nu exista idEntitate
        :param idEntitate:
        :return: lista de entitati sau None daca idEntitate=None
        """
        if idEntitate is None:
            return list(self.entitati.values())
        if idEntitate in self.entitati:
            return self.entitati[idEntitate]
        else:
            return None

    def adauga(self, entitate: Entitate) -> None:
        """
        adauga o noua entitate
        :param entitate: poate fi masina, card client sau tranzactie
        :return: -
        """
        if self.read(entitate.idEntitate) is not None:
            raise KeyError("Exista deja o entitate cu id-ul dat!")
        self.entitati[entitate.idEntitate] = entitate

    def sterge(self, idEntitate: str) -> None:
        """
        sterge entiatea cu id-ul dat
        :param idEntitate: id-ul entitatii
        :return: -
        """
        if self.read(idEntitate) is None:
            raise KeyError("Nu exista nicio entitate cu id-ul dat!")
        del self.entitati[idEntitate]

    def modifica(self, entitate: Entitate) -> None:
        """
        modifica o entitate deja existenta
        :param entitate: entitatea data
        :return: -
        """
        if self.read(entitate.idEntitate) is None:
            raise KeyError("Nu exista nicio entitate cu id-ul dat!")
        self.entitati[entitate.idEntitate] = entitate

import random

from Domain.addOperation import AddOperation
from Domain.deleteOperation import DeleteOperation
from Domain.masina import Masina
from Domain.masinaValidator import MasinaValidator
from Domain.modifyOperation import ModifyOperation
from Repository.repository import Repository
from Service.undoRedoService import UndoRedoService


class MasinaService:
    def __init__(self, masinaRepository: Repository,
                 masinaValidator: MasinaValidator,
                 undoRedoService: UndoRedoService):
        self.__masinaRepository = masinaRepository
        self.__masinaValidator = masinaValidator
        self.__undoRedoService = undoRedoService

    def getAll(self):
        """
        da masinile existente
        :return: -
        """
        return self.__masinaRepository.read()

    def adauga(self, idMasina, model, anAchizitie, nrKm, inGarantie):
        """
        adauga o masina noua
        :param idMasina: string, id-ul masinii
        :param model: string, modelul masinii
        :param anAchizitie: int, anul achizitiei masinii
        :param nrKm: float, numarul de km al masinii
        :param inGarantie: string, trebuie sa fie 'da' sau 'nu'
        :return: -
        """
        masina = Masina(idMasina, model, anAchizitie, nrKm, inGarantie)
        self.__masinaValidator.valideaza(masina)
        self.__masinaRepository.adauga(masina)
        self.__undoRedoService.addUndoRedoOperation(
            AddOperation(self.__masinaRepository, masina))

    def sterge(self, idMasina) -> None:
        """
        sterge masina cu id-ul dat
        :param idMasina: id-ul masinii de sters
        :return: -
        """
        masinaStearsa = self.__masinaRepository.read(idMasina)
        self.__masinaRepository.sterge(idMasina)
        self.__undoRedoService.addUndoRedoOperation(
            DeleteOperation(self.__masinaRepository, masinaStearsa))

    def modifica(self, idMasina, model, anAchizitie, nrKm, inGarantie) -> None:
        """
        modifica o masina existenta
        :param idMasina: string, id-ul masinii
        :param model: string, modelul masinii
        :param anAchizitie: int, anul achizitiei masinii
        :param nrKm: float, numarul de km al masinii
        :param inGarantie: string, trebuie sa fie 'da' sau 'nu'
        :return: -
        """
        masinaVeche = self.__masinaRepository.read(idMasina)
        masina = Masina(idMasina, model, anAchizitie, nrKm, inGarantie)
        self.__masinaValidator.valideaza(masina)
        self.__masinaRepository.modifica(masina)
        self.__undoRedoService.addUndoRedoOperation(
            ModifyOperation(self.__masinaRepository, masinaVeche, masina))

    def findById(self, val):
        masini = self.getAll()
        for masina in masini:
            if val == masina.idEntitate:
                return masina

    def generareMasiniRandom(self, n) -> None:
        listaModel = ["BMW", "Audi", "Opel",
                      "Ford", "Renault", "Volvo"]
        listaInGarantie = ["da", "nu"]
        for i in range(n):
            try:
                idMasina = str(random.randint(100, 1000))
                model = random.choice(listaModel)
                anAchizitie = random.randint(2000, 2021)
                nrKm = random.uniform(10000.0, 100000.0)
                inGarantie = random.choice(listaInGarantie)

                self.adauga(
                    idMasina, model, anAchizitie, nrKm, inGarantie)
            except Exception as e:
                print(e)

    def cautareFullTextMasini(self, text) -> list:
        """
        cauta un string in entitatile: masini si clienti
        :return: o lista de entitati(masini si clienti)
        ce contin stringul dat
        """
        try:
            '''masini = self.getAll()
            entitati = []
            for masina in masini:
                if text in str(masina.model) or \
                        text in str(masina.inGarantie) \
                        or text in str(masina.idEntitate) \
                        or text in str(masina.nrKm) or \
                        text in str(masina.anAchizitie):
                    entitati.append(masina)
            return entitati'''
            rezultat = self.__masinaRepository.read()
            return list(filter(lambda x: text in x.model or
                        text in x.inGarantie or text in str(x.nrKm), rezultat))
        except Exception as e:
            print(e)

    def actualizareGarantie(self):
        """
        Modificarea garanției la fiecare mașină:
        o mașină este în garanție dacă și numai dacă
        are maxim 3 ani de la achiziție și maxim 60 000 de km.
        :return: -
        """
        try:
            masini = self.getAll()
            for masina in masini:
                if masina.nrKm <= 60000 and masina.anAchizitie >= 2018:
                    masina.inGarantie = "da"
                else:
                    masina.inGarantie = "nu"
                idEntitate = masina.idEntitate
                model = masina.model
                anAchizitie = masina.anAchizitie
                nrKm = masina.nrKm
                inGarantie = masina.inGarantie
                masinaVeche = self.__masinaRepository.read(masina.idEntitate)
                self.modifica(
                    idEntitate, model, anAchizitie, nrKm, inGarantie)
                self.__undoRedoService.addUndoRedoOperation(
                    ModifyOperation(self.__masinaRepository,
                                    masinaVeche, masina))
        except Exception as e:
            print(e)

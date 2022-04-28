from datetime import datetime

from datetimerange import DateTimeRange

from Domain.addOperation import AddOperation
from Domain.deleteOperation import DeleteOperation
from Domain.modifyOperation import ModifyOperation
from Domain.multiDeleteCascada import MultiDeleteCascada
from Domain.multiDeleteOperation import MultiDelete
from Domain.tranzactie import Tranzactie
from Domain.tranzactieValidator import TranzactieValidator
from Repository.repository import Repository
from Service.cardClientiService import CardClientService
from Service.masinaService import MasinaService
from Service.undoRedoService import UndoRedoService


class TranzactieService:
    def __init__(self, tranzactieRepository: Repository,
                 tranzactieValidator: TranzactieValidator,
                 masinaRepository: Repository,
                 cardClientRepository: Repository,
                 masinaService: MasinaService,
                 cardClientService: CardClientService,
                 undoRedoService: UndoRedoService):
        self.__masinaRepository = masinaRepository
        self.__cardClientRepository = cardClientRepository
        self.__tranzactieRepository = tranzactieRepository
        self.__tranzactieValidator = tranzactieValidator
        self.__masinaService = masinaService
        self.__cardClientService = cardClientService
        self.__undoRedoService = undoRedoService

    def getAll(self):
        """
        da tranzactile existente
        :return: -
        """
        return self.__tranzactieRepository.read()

    def adauga(self, idTranzactie, idMasina,
               idCard, sumaPiese, manopera, dataOra):
        """
        adauga o tranzactie noua
        :param idTranzactie: string, id-ul tranzactiei
        :param idMasina: string, id-ul masinii
        :param idCard: string, id-ul cardului sau None
        :param sumaPiese: float, suma pieselor
        :param manopera: float, costul manoperei
        :param dataOra: datetime, data si ora tranzactiei
        :return: -
        """
        tranzactie = Tranzactie(idTranzactie,
                                idMasina, idCard, sumaPiese, manopera, dataOra)
        if self.__masinaRepository.getById(idMasina) is None:
            raise ValueError(
                "Nu exista masina cu idMasina introdus!!")
        if self.reducereSuma(idMasina) is True:
            tranzactie.sumaPiese = 0
        if tranzactie.idCard != '':
            tranzactie.manopera = tranzactie.manopera \
                                  - (10 / 100 * tranzactie.manopera)
        self.__tranzactieValidator.valideaza(tranzactie)
        self.__tranzactieRepository.adauga(tranzactie)
        self.__undoRedoService.addUndoRedoOperation(
            AddOperation(self.__tranzactieRepository, tranzactie)
        )

    def sterge(self, idTranzactie) -> None:
        """
        sterge o tranzactie
        :param idTranzactie: id-ul tranzactiei
        :return:
        """
        tranzactieSters = self.__tranzactieRepository.read(idTranzactie)
        self.__tranzactieRepository.sterge(idTranzactie)
        self.__undoRedoService.addUndoRedoOperation(
            DeleteOperation(self.__tranzactieRepository,
                            tranzactieSters))

    def modifica(self, idTranzactie,
                 idMasina, idCard, sumaPiese, manopera, dataOra) -> None:
        """
        modifica o tranzactie
        :param idTranzactie: string, id-ul tranzactiei
        :param idMasina: string, id-ul masinii
        :param idCard: string, id-ul cardului sau None
        :param sumaPiese: float, suma pieselor
        :param manopera: float, costul manoperei
        :param dataOra: datetime, data si ora tranzactiei
        :return: -
        """
        tranzactieVeche = self.__tranzactieRepository.read(idTranzactie)
        tranzactie = Tranzactie(
            idTranzactie, idMasina, idCard, sumaPiese, manopera, dataOra)
        self.__tranzactieValidator.valideaza(tranzactie)
        self.__tranzactieRepository.modifica(tranzactie)
        self.__undoRedoService.addUndoRedoOperation(
            ModifyOperation(self.__tranzactieRepository,
                            tranzactieVeche, tranzactie))

    def reducereSuma(self, idMasina) -> bool:
        """
        daca masina este in garantie, atunci reducerea este posibila
        :param idMasina: id-ul masinii
        :return: True, daca se poate realiza reducerea
        sau False in caz contrar
        """
        masina = self.__masinaRepository.getById(idMasina)
        if masina.inGarantie == "da":
            return True
        return False

    def treanzactiiSumaInterval(self, suma1, suma2, tranzactii: list,
                                rezultat: list) -> list:
        """
        afiseaza toate tranzacțiile cu suma cuprinsă într-un interval dat
        :param suma1: capat de interval
        :param suma2: capat de interval
        :param tranzactii: tranzactiile
        :param rezultat: lista de afisat
        :return: o lista ce contine tranzacțiile
        cu suma cuprinsă într-un interval dat
        """
        try:
            ''' lista = []
            for tranzactie in tranzactii:
                if suma1 < tranzactie.sumaPiese < suma2:
                    lista.append(tranzactie)'''

            '''lista = [x for x in tranzactii if suma1 < x.sumaPiese < suma2]
            return lista'''

            if len(tranzactii) == 1:
                if suma1 <= tranzactii[0].sumaPiese <= suma2:
                    rezultat.append(tranzactii[0])
            else:
                if suma1 <= tranzactii[0].sumaPiese <= suma2:
                    rezultat.append(tranzactii[0])
                self.treanzactiiSumaInterval(suma1, suma2, tranzactii[1:],
                                             rezultat)
            return rezultat
        except Exception as e:
            print(e)

    def strgereTranzactiiInterval(self, data1, data2) -> None:
        """
        sterge toate tranzacțiile dintr-un
        anumit interval de zile
        :param data1: capat de interval
        :param data2: capat de inerval
        :return: -
        """
        try:
            datetime.strptime(data1, '%d.%m.%Y %H:%M')
            datetime.strptime(data2, '%d.%m.%Y %H:%M')
            tranzactii = self.getAll()
            interval = DateTimeRange(data1, data2)
            tranzactieStearsa = []
            for tranzactie in tranzactii:
                if tranzactie.dataOra in interval:
                    tranzactieStearsa.append(tranzactie)
                    self.sterge(tranzactie.idEntitate)
                self.__undoRedoService.addUndoRedoOperation(
                    MultiDelete(self.__tranzactieRepository,
                                tranzactieStearsa))
        except Exception as e:
            print(e)

    def findById(self, val):
        tranzactii = self.getAll()
        for tranzactie in tranzactii:
            if val == tranzactie.idEntitate:
                return tranzactie

    def sortaree(self, iterable, key, reverse: bool):
        if reverse is False:
            for i in range(len(iterable) - 1):
                if key(iterable[i]) > key(iterable[i + 1]):
                    iterable[i], iterable[i + 1] = iterable[i + 1], iterable[i]
        else:
            for i in range(len(iterable) - 1):
                if key(iterable[i]) < key(iterable[i + 1]):
                    iterable[i], iterable[i + 1] = iterable[i + 1], iterable[i]
        return iterable

    def ordoneazaMasiniDupaSuma(self) -> list[dict[str, list | None]]:
        """
        ordoneaza masinile descrescator dupa suma manoperei
        :return: -
        """
        sumeManopera = {}
        for masina in self.__masinaRepository.read():
            sumeManopera[masina.idEntitate] = []
        for tranzactie in self.__tranzactieRepository.read():
            if tranzactie.idMasina in sumeManopera:
                sumeManopera[tranzactie.idMasina].append(tranzactie.manopera)

        rezultat = []
        for idMasina in sumeManopera:
            sume = sumeManopera[idMasina]
            rezultat.append(
                {
                    "masina": self.__masinaRepository.read(idMasina),
                    "sumaManopera": sume
                }
            )
        return self.sortaree(
            rezultat,
            key=lambda sumaManopera: sumaManopera["sumaManopera"],
            reverse=True)

    def ordoneazaCarduriDupaReducere(self) -> list[dict[str, list | None]]:
        """
        ordoneaza cardurile descrescator dupa reducere
        :return: -
        """
        reduceri = {}
        for card in self.__cardClientRepository.read():
            reduceri[card.idEntitate] = []
        for tranzactie in self.__tranzactieRepository.read():
            if tranzactie.idCard != '':
                total = (10 * tranzactie.manopera) / 9
                reduceri[tranzactie.idCard].append(total * 10 / 100)

        rezultat = []
        for idCard in reduceri:
            red = reduceri[idCard]
            rezultat.append(
                {
                    "cardClient": self.__cardClientRepository.read(idCard),
                    "reducere": red
                }
            )
        return sorted(
            rezultat,
            key=lambda reducere: reducere["reducere"],
            reverse=True)

    def stergereMasiniCascada(self, idMasina) -> None:
        """
        stergere in cascada de masini si tranzactii
        :param idMasina: id-ul masinii
        :return:
        """
        try:
            masinaStearsa = []
            tranzactieStearsa = []
            for masina in self.__masinaRepository.read():
                if str(masina.idEntitate) == str(idMasina):
                    masinaStearsa.append(
                        self.__masinaRepository.read(masina.idEntitate))
                    self.__masinaService.sterge(idMasina)

                    for tranzactie in self.__tranzactieRepository.read():
                        if str(tranzactie.idMasina) == str(idMasina):
                            tranzactieStearsa.append(
                                self.__tranzactieRepository.read(
                                    tranzactie.idEntitate))
                            self.sterge(tranzactie.idEntitate)
                            self.__undoRedoService.addUndoRedoOperation(
                                MultiDeleteCascada(self.__masinaRepository,
                                                   self.__tranzactieRepository,
                                                   masinaStearsa,
                                                   tranzactieStearsa))
        except Exception as e:
            print(e)

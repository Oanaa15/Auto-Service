from Domain.addOperation import AddOperation
from Domain.cardClient import CardClient
from Domain.cardClientValidator import CardClientValidator
from Domain.deleteOperation import DeleteOperation
from Domain.modifyOperation import ModifyOperation
from Repository.repository import Repository
from Service.undoRedoService import UndoRedoService


class CardClientService:
    def __init__(self,
                 cardClientRepository: Repository,
                 cardClientValidator: CardClientValidator,
                 undoRedoService: UndoRedoService):
        self.__cardClientRepository = cardClientRepository
        self.__cardClientValidator = cardClientValidator
        self.__undoRedoService = undoRedoService

    def getAll(self):
        """
        da cardurile client existente
        :return: -
        """
        return self.__cardClientRepository.read()

    def adauga(self, idCard, nume, prenume,
               cnp, dataNastere, dataInreg) -> None:
        """
        adauga un card client nou
        :param idCard: string, id-ul cardului
        :param nume: string, numele clientului
        :param prenume: string, prenumele clientului
        :param cnp: string, cnp-ul clientului
        :param dataNastere: tipul datetime, data nasterii
        :param dataInreg: tipul datetime, data inregistrarii
        :return: -
        """
        card = CardClient(idCard, nume, prenume, cnp, dataNastere, dataInreg)
        self.__cardClientValidator.valideaza(card)
        for card2 in self.getAll():
            if cnp == card2.cnp:
                raise KeyError("Exista deja un card cu acest CNP !! ")
        self.__cardClientRepository.adauga(card)
        self.__undoRedoService.addUndoRedoOperation(
            AddOperation(self.__cardClientRepository, card))

    def sterge(self, idCard) -> None:
        """
        sterge un card client
        :param idCard: string, id-ul cardului de sters
        :return:
        """
        cardSters = self.__cardClientRepository.read(idCard)
        self.__cardClientRepository.sterge(idCard)
        self.__undoRedoService.addUndoRedoOperation(
            DeleteOperation(self.__cardClientRepository, cardSters))

    def modifica(self, idCard, nume,
                 prenume, cnp, dataNastere, dataInreg) -> None:
        """
        modifica un card client deja existent
        :param idCard: string, id-ul cardului
        :param nume: string, numele clientului
        :param prenume: string, prenumele clientului
        :param cnp: string, cnp-ul clientului
        :param dataNastere: tipul datetime, data nasterii
        :param dataInreg: tipul datetime, data inregistrarii
        :return: -
        """
        cardVechi = self.__cardClientRepository.read(idCard)
        card = CardClient(idCard, nume, prenume, cnp, dataNastere, dataInreg)
        self.__cardClientValidator.valideaza(card)
        self.__cardClientRepository.modifica(card)
        self.__undoRedoService.addUndoRedoOperation(
            ModifyOperation(self.__cardClientRepository, cardVechi, card))

    def findById(self, val):
        carduri = self.getAll()
        for card in carduri:
            if val == card.idEntitate:
                return card

    def cautareFullTextClienti(self, text) -> list:
        """
        cauta un string in entitatile: masini si clienti
        :return: o lista de entitati(masini si clienti)
        ce contin stringul dat
        """
        '''entitati = []
        carduri = self.getAll()
        for card in carduri:
            if text in str(card.nume) or text in str(card.prenume) or \
                    text in str(card.idEntitate) \
                    or text in str(card.cnp) or text in str(card.dataNastere) \
                    or text in str(card.dataInreg):
                entitati.append(card)
        return entitati'''
        try:
            rezultat = self.__cardClientRepository.read()
            return list(filter(lambda x:
                               text in x.nume or text in x.prenume or text
                               in str(x.cnp)
                               or text in str(x.dataInreg) or text in
                               str(x.dataNastere), rezultat))
        except Exception as e:
            print(e)

from Domain.cardClientValidator import CardClientValidator
from Repository.repositoryJson import RepositoryJson
from Service.cardClientiService import CardClientService
from Service.undoRedoService import UndoRedoService
from Tests.utilFile import clearFile


def testAdaugaCard():
    clearFile("serviceCardTest.txt")
    repository = RepositoryJson("serviceCardTest.txt")
    cardClientValidator = CardClientValidator()
    undoRedoService = UndoRedoService()
    cardService = CardClientService(repository, cardClientValidator,
                                    undoRedoService)

    cardService.adauga(
        '1', 'petre', 'andreea', '1234567', '12.12.2001', '14.10.2012')
    cardService.adauga(
        '2', 'lechea', 'aura', '987654356', '08.12.2002', '19.02.2020')

    card1 = repository.getById('1')
    card2 = repository.getById('2')

    assert card1.idEntitate == '1'
    assert card1.nume == 'petre'
    assert card1.prenume == 'andreea'
    assert card1.cnp == '1234567'
    assert card1.dataNastere == '12.12.2001'
    assert card1.dataInreg == '14.10.2012'

    assert card2.idEntitate == '2'
    assert card2.nume == 'lechea'
    assert card2.prenume == 'aura'
    assert card2.cnp == '987654356'
    assert card2.dataNastere == '08.12.2002'
    assert card2.dataInreg == '19.02.2020'


def testStergeCard():
    clearFile("serviceCardTest.txt")
    repository = RepositoryJson("serviceCardTest.txt")
    cardClientValidator = CardClientValidator()
    undoRedoService = UndoRedoService()
    cardService = CardClientService(repository, cardClientValidator,
                                    undoRedoService)

    cardService.adauga(
        '1', 'petre', 'andreea', '1234567', '12.12.2001', '14.10.2012')
    cardService.adauga(
        '2', 'lechea', 'aura', '9876543', '08.12.2002', '19.02.2020')

    assert len(cardService.getAll()) == 2
    cardService.sterge('1')
    card1 = repository.getById('1')
    card2 = repository.getById('2')
    assert len(cardService.getAll()) == 1
    assert card1 is None
    assert card2 is not None
    assert card2.idEntitate == '2'
    assert card2.nume == 'lechea'
    assert card2.dataNastere == '08.12.2002'
    assert card2.dataInreg == '19.02.2020'
    cardService.sterge('2')
    assert len(cardService.getAll()) == 0


def testModificaCard():
    clearFile("serviceCardTest.txt")
    repository = RepositoryJson("serviceCardTest.txt")
    cardClientValidator = CardClientValidator()
    undoRedoService = UndoRedoService()
    cardService = CardClientService(
        repository, cardClientValidator, undoRedoService)

    cardService.adauga(
        '1', 'petre', 'andreea', '1234567', '12.12.2001', '14.10.2012')
    cardService.adauga(
        '2', 'lechea', 'aura', '9876543', '08.12.2002', '19.02.2020')

    cardService.modifica(
        '2', 'andrei', 'aura', '565656', '08.01.2000', '19.02.2020')
    card2 = repository.getById('2')
    assert card2.idEntitate == '2'
    assert card2.nume == 'andrei'
    assert card2.prenume == 'aura'
    assert card2.cnp == '565656'
    assert card2.dataNastere == '08.01.2000'
    assert card2.dataInreg == '19.02.2020'

    cardService.modifica(
        '1', 'petre', 'alin', '565656', '08.01.2000', '19.02.2020')
    card2 = repository.getById('1')
    assert card2.idEntitate == '1'
    assert card2.nume == 'petre'
    assert card2.prenume == 'alin'
    assert card2.cnp == '565656'
    assert card2.dataNastere == '08.01.2000'
    assert card2.dataInreg == '19.02.2020'

from Domain.addOperation import AddOperation
from Domain.cardClientValidator import CardClientValidator
from Domain.masinaValidator import MasinaValidator
from Repository.repositoryJson import RepositoryJson
from Service.cardClientiService import CardClientService
from Service.masinaService import MasinaService
from Service.undoRedoService import UndoRedoService
from Tests.utilFile import clearFile


def testAdaugaMasina():
    clearFile("serviceTest.txt")
    repository = RepositoryJson("serviceTest.txt")
    masinaValidator = MasinaValidator()
    undoRedoService = UndoRedoService()
    masinaService = MasinaService(repository, masinaValidator, undoRedoService)
    masinaService.adauga('1', 'dacia', 2011, 100000.0, 'nu')
    masinaService.adauga('2', 'audi', 2019, 20500.0, 'da')

    masina1 = repository.getById('1')
    masina2 = repository.getById('2')

    assert masina1.idEntitate == '1'
    assert masina1.model == 'dacia'
    assert masina1.anAchizitie == 2011
    assert masina1.nrKm == 100000
    assert masina1.inGarantie == 'nu'

    assert masina2.idEntitate == '2'
    assert masina2.model == 'audi'
    assert masina2.anAchizitie == 2019
    assert masina2.nrKm == 20500
    assert masina2.inGarantie == 'da'


def testStergeMasina():
    clearFile("serviceTest.txt")
    repository = RepositoryJson("serviceTest.txt")
    masinaValidator = MasinaValidator()
    undoRedoService = UndoRedoService()
    masinaService = MasinaService(repository, masinaValidator, undoRedoService)
    masinaService.adauga('1', 'dacia', 2011, 100000.0, 'nu')
    masinaService.adauga('2', 'audi', 2019, 20500.0, 'da')

    assert len(masinaService.getAll()) == 2

    masinaService.sterge('2')
    masina1 = repository.getById('1')
    masina2 = repository.getById('2')
    assert len(masinaService.getAll()) == 1
    assert masina2 is None
    assert masina1 is not None
    assert masina1.model == 'dacia'
    assert masina1.nrKm == 100000
    assert masina1.inGarantie == 'nu'
    masinaService.sterge('1')
    assert len(masinaService.getAll()) == 0


def testModificareMasina():
    clearFile("serviceTest.txt")
    repository = RepositoryJson("serviceTest.txt")
    masinaValidator = MasinaValidator()
    undoRedoService = UndoRedoService()
    masinaService = MasinaService(repository,
                                  masinaValidator,
                                  undoRedoService)
    masinaService.adauga('1', 'dacia', 2011, 100000.0, 'nu')
    masinaService.adauga('2', 'audi', 2019, 20500.0, 'da')

    masinaService.modifica('1', 'audi', 2012, 100000.0, 'nu')

    masina1 = repository.getById('1')
    masina2 = repository.getById('2')

    assert masina1.idEntitate == '1'
    assert masina1.model == 'audi'
    assert masina1.anAchizitie == 2012
    assert masina1.nrKm == 100000
    assert masina1.inGarantie == 'nu'
    assert masina2.model == 'audi'
    assert masina2.anAchizitie == 2019
    assert masina2.inGarantie == 'da'

    masinaService.modifica('2', 'audi', 2012, 100000.0, 'nu')
    masina2 = repository.getById('2')

    assert masina2.idEntitate == '2'
    assert masina2.model == 'audi'
    assert masina2.anAchizitie == 2012
    assert masina2.nrKm == 100000
    assert masina2.inGarantie == 'nu'


def testCautareText():
    clearFile("serviceMasiniTest.txt")
    repositoryM = RepositoryJson("serviceMasiniTest.txt")
    masinaValidator = MasinaValidator()
    undoRedoService = UndoRedoService()
    masinaService = MasinaService(repositoryM,
                                  masinaValidator,
                                  undoRedoService)

    clearFile("serviceCardTest.txt")
    cardClientValidator = CardClientValidator()
    repositoryC = RepositoryJson("serviceCardTest.txt")
    cardService = CardClientService(repositoryC,
                                    cardClientValidator,
                                    undoRedoService)

    masinaService.adauga('1', 'dacia', 2011, 100000.0, 'nu')
    masinaService.adauga('2', 'audi', 2019, 20500.0, 'da')

    cardService.adauga(
        '3', 'petre', 'andreea', '1234567', '12.12.2001', '14.10.2012')
    cardService.adauga(
        '4', 'lechea', 'aura', '9876543', '08.12.2002', '19.02.2020')

    text = 'dac'
    val1 = masinaService.findById('1')
    assert val1 in masinaService.cautareFullTextMasini(text)

    text2 = 'ea'
    val2 = cardService.findById('3')
    val3 = cardService.findById('4')
    assert val2 in cardService.cautareFullTextClienti(text2)
    assert val3 in cardService.cautareFullTextClienti(text2)


def testGenerareMasini():
    clearFile("serviceMasiniTest.txt")
    repositoryM = RepositoryJson("serviceMasiniTest.txt")
    masinaValidator = MasinaValidator()
    undoRedoService = UndoRedoService()
    masinaService = MasinaService(repositoryM, masinaValidator,
                                  undoRedoService)

    nrMasini = 4
    masinaService.generareMasiniRandom(nrMasini)
    assert len(masinaService.getAll()) == 4


def testActualizareGarantie():
    clearFile("serviceMasiniTest.txt")
    repository = RepositoryJson("serviceMasiniTest.txt")
    masinaValidator = MasinaValidator()
    undoRedoService = UndoRedoService()
    masinaService = MasinaService(repository, masinaValidator,
                                  undoRedoService)

    masinaService.adauga('1', 'dacia', 2011, 100000.0, 'da')
    masinaService.adauga('2', 'audi', 2019, 20500.0, 'nu')

    masinaService.actualizareGarantie()
    masina1 = repository.getById('1')
    masina2 = repository.getById('2')

    assert masina1.inGarantie == 'nu'
    assert masina2.inGarantie == 'da'

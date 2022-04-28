from Domain.cardClientValidator import CardClientValidator
from Domain.masinaValidator import MasinaValidator
from Domain.tranzactieValidator import TranzactieValidator
from Repository.repositoryJson import RepositoryJson
from Service.cardClientiService import CardClientService
from Service.masinaService import MasinaService
from Service.tranzactieService import TranzactieService
from Service.undoRedoService import UndoRedoService
from Tests.utilFile import clearFile


def testUndoRedo():
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

    undoRedoService.undo()
    assert len(masinaService.getAll()) == 1

    undoRedoService.redo()
    assert len(masinaService.getAll()) == 2
    assert masina2.idEntitate == '2'
    assert masina2.model == 'audi'
    assert masina2.anAchizitie == 2019
    assert masina2.nrKm == 20500
    assert masina2.inGarantie == 'da'

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

    undoRedoService.undo()
    assert len(cardService.getAll()) == 1
    assert card2.idEntitate == '2'
    assert card2.nume == 'lechea'
    assert card2.dataNastere == '08.12.2002'
    assert card2.dataInreg == '19.02.2020'

    undoRedoService.redo()
    assert len(cardService.getAll()) == 0

    undoRedoService = UndoRedoService()
    clearFile("serviceTranzactiiTest.txt")
    tranzactieRepository = RepositoryJson(
        "serviceTranzactiiTest.txt")

    clearFile("serviceCardTest.txt")
    cardClientValidator = CardClientValidator()
    cardClientRepository = RepositoryJson("serviceCardTest.txt")
    cardService = CardClientService(cardClientRepository,
                                    cardClientValidator,
                                    undoRedoService)

    clearFile("serviceMasiniTest.txt")
    masinaRepository = RepositoryJson("serviceMasiniTest.txt")
    masinaValidator = MasinaValidator()
    masinaService = MasinaService(masinaRepository, masinaValidator,
                                  undoRedoService)

    tranzactieValidator = TranzactieValidator()
    tranzactieService = TranzactieService(tranzactieRepository,
                                          tranzactieValidator,
                                          masinaRepository,
                                          cardClientRepository,
                                          masinaService,
                                          cardService,
                                          undoRedoService)

    masinaService.adauga('1', 'dacia', 2011, 100000.0, 'nu')
    cardService.adauga('1', 'petre', 'andreea',
                       '1234567', '12.12.2001', '14.10.2012')

    tranzactieService.adauga('1', '1', '', 200, 180,
                             '12.12.2020 14:15')
    tranzactieService.modifica('1', '1', '', 90, 180,
                               '14.10.2012 11:10')
    tranzactie1 = tranzactieRepository.getById('1')

    assert tranzactie1.idEntitate == '1'
    assert tranzactie1.idMasina == '1'
    assert tranzactie1.idCard == ''
    assert tranzactie1.sumaPiese == 90
    assert tranzactie1.manopera == 180
    assert tranzactie1.dataOra == '14.10.2012 11:10'

    undoRedoService.undo()
    tranzactie1 = tranzactieRepository.getById('1')
    assert tranzactie1.idEntitate == '1'
    assert tranzactie1.idMasina == '1'
    assert tranzactie1.idCard == ''
    assert tranzactie1.sumaPiese == 200
    assert tranzactie1.manopera == 180
    assert tranzactie1.dataOra == '12.12.2020 14:15'

    undoRedoService.redo()
    tranzactie1 = tranzactieRepository.getById('1')
    assert tranzactie1.idEntitate == '1'
    assert tranzactie1.idMasina == '1'
    assert tranzactie1.idCard == ''
    assert tranzactie1.sumaPiese == 90
    assert tranzactie1.manopera == 180
    assert tranzactie1.dataOra == '14.10.2012 11:10'

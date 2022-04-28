from Domain.cardClientValidator import CardClientValidator
from Domain.masinaValidator import MasinaValidator
from Domain.tranzactieValidator import TranzactieValidator
from Repository.repositoryJson import RepositoryJson
from Service.cardClientiService import CardClientService
from Service.masinaService import MasinaService
from Service.tranzactieService import TranzactieService
from Service.undoRedoService import UndoRedoService
from Tests.utilFile import clearFile


def testAdaugareTranzactie():
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

    tranzactieService.adauga('1', '1', '1', 200,
                             180, '12.12.2020 14:15')
    tranzactie1 = tranzactieRepository.getById('1')

    assert tranzactie1.idEntitate == '1'
    assert tranzactie1.idMasina == '1'
    assert tranzactie1.idCard == '1'
    assert tranzactie1.sumaPiese == 200
    assert tranzactie1.manopera == 162  # a fost aplica reducere
    assert tranzactie1.dataOra == '12.12.2020 14:15'

    masinaService.adauga('2', 'audi', 2019, 20500.0, 'da')
    tranzactieService.adauga('2', '2', '', 1000,
                             250, '12.12.2020 10:25')
    tranzactie2 = tranzactieRepository.getById('2')

    assert tranzactie2.idEntitate == '2'
    assert tranzactie2.idMasina == '2'
    assert tranzactie2.idCard == ''
    assert tranzactie2.sumaPiese == 0
    assert tranzactie2.manopera == 250
    assert tranzactie2.dataOra == '12.12.2020 10:25'


def testStergeTranzactie():
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
    tranzactieService.adauga('1', '1', '1', 200, 180,
                             '12.12.2020 14:15')

    masinaService.adauga('2', 'audi', 2019, 20500.0, 'da')
    tranzactieService.adauga('2', '2', '', 1000, 250,
                             '12.12.2020 10:25')

    assert len(tranzactieService.getAll()) == 2
    tranzactieService.sterge('1')
    tranzactie1 = tranzactieRepository.getById('1')
    tranzactie2 = tranzactieRepository.getById('2')
    assert len(tranzactieService.getAll()) == 1
    assert tranzactie1 is None
    assert tranzactie2 is not None
    assert tranzactie2.idEntitate == '2'
    assert tranzactie2.idMasina == '2'
    assert tranzactie2.idCard == ''
    tranzactieService.sterge('2')
    assert len(tranzactieService.getAll()) == 0


def testModificaTranzactie():
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

    tranzactieService.adauga('1', '1', '1', 200, 180,
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

    masinaService.adauga('2', 'audi', 2019, 20500.0, 'da')
    tranzactieService.adauga('2', '2', '', 1000, 250,
                             '12.12.2020 10:25')
    tranzactieService.modifica('2', '2', '', 90, 180,
                               '14.11.2012 11:10')
    tranzactie2 = tranzactieRepository.getById('2')

    assert tranzactie2.idEntitate == '2'
    assert tranzactie2.idMasina == '2'
    assert tranzactie2.idCard == ''
    assert tranzactie2.sumaPiese == 90
    assert tranzactie2.manopera == 180
    assert tranzactie2.dataOra == '14.11.2012 11:10'


def testStergereTranzactiiInterval():
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

    tranzactieService.adauga('1', '1', '1', 200, 180,
                             '12.12.2017 14:15')
    masinaService.adauga('2', 'audi', 2019, 20500.0, 'da')
    tranzactieService.adauga('2', '2', '', 1000, 250,
                             '12.12.2020 10:25')
    data1 = '10.11.2016 14:15'
    data2 = '12.12.2018 14:15'
    tranzactieService.strgereTranzactiiInterval(data1, data2)

    tranzactieStearsa = tranzactieRepository.getById('1')
    tranzactieRamasa = tranzactieRepository.getById('2')
    assert tranzactieStearsa is None
    assert tranzactieRamasa is not None


def testStergereMasiniCascada():
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

    tranzactieService.adauga('1', '1', '1', 200, 180,
                             '12.12.2017 14:15')
    masinaService.adauga('2', 'audi', 2019, 20500.0, 'da')
    tranzactieService.adauga('2', '2', '', 1000, 250,
                             '12.12.2020 10:25')

    tranzactieService.stergereMasiniCascada('1')
    tranzactie1 = tranzactieRepository.getById('1')
    masina1 = masinaRepository.getById('1')

    assert masina1 is None
    assert tranzactie1 is None

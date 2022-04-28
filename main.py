from Domain.cardClientValidator import CardClientValidator
from Domain.masinaValidator import MasinaValidator
from Domain.tranzactieValidator import TranzactieValidator
from Repository.repositoryJson import RepositoryJson
from Service.cardClientiService import CardClientService
from Service.masinaService import MasinaService
from Service.tranzactieService import TranzactieService
from Service.undoRedoService import UndoRedoService
from Tests.testAll import runAllTests
from UI.consola import Consola


def main():
    runAllTests()

    undoRedoService = UndoRedoService()

    masinaRepositoryJson = RepositoryJson("masini.json")
    masinaValidator = MasinaValidator()
    masinaService = MasinaService(masinaRepositoryJson,
                                  masinaValidator,
                                  undoRedoService)

    cardClientRepositoryJson = RepositoryJson("cardClient.json")
    cardClientValidator = CardClientValidator()
    cardClientService = CardClientService(
        cardClientRepositoryJson, cardClientValidator, undoRedoService)

    tranzactieRepositoryJson = RepositoryJson("tranzactie.json")
    tranzactieValidator = TranzactieValidator()
    tranzactieService = TranzactieService(tranzactieRepositoryJson,
                                          tranzactieValidator,
                                          masinaRepositoryJson,
                                          cardClientRepositoryJson,
                                          masinaService,
                                          cardClientService,
                                          undoRedoService)
    consola = Consola(masinaService,
                      cardClientService,
                      tranzactieService,
                      undoRedoService)
    consola.runMenu()


if __name__ == '__main__':
    main()

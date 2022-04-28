from Tests.domainTest import testMasina, testCardClient, testTranzactie
from Tests.repositoryTest import adaugareTest, \
    stergereTest, modificaTest
from Tests.testCardService import testAdaugaCard, \
    testStergeCard, testModificaCard
from Tests.testMasinaService import \
    testCautareText, testAdaugaMasina, \
    testStergeMasina, testModificareMasina, \
    testGenerareMasini, testActualizareGarantie
from Tests.testTranzactieService import \
    testAdaugareTranzactie, testStergeTranzactie, \
    testModificaTranzactie, testStergereTranzactiiInterval, \
    testStergereMasiniCascada
from Tests.testUndoRedo import testUndoRedo


def runAllTests():
    testMasina()
    testCardClient()
    testTranzactie()
    adaugareTest()
    stergereTest()
    modificaTest()

    testAdaugaMasina()
    testStergeMasina()
    testModificareMasina()
    testCautareText()
    testGenerareMasini()
    testActualizareGarantie()

    testAdaugaCard()
    testStergeCard()
    testModificaCard()

    testAdaugareTranzactie()
    testStergeTranzactie()
    testModificaTranzactie()
    testStergereTranzactiiInterval()

    testStergereMasiniCascada()

    testUndoRedo()

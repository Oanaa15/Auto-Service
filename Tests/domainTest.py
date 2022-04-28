from Domain.cardClient import CardClient
from Domain.masina import Masina
from Domain.tranzactie import Tranzactie


def testMasina():
    masina = Masina('1', 'dacia', 2011, 100000, 'nu')
    assert masina.idEntitate == '1'
    assert masina.model == 'dacia'
    assert masina.anAchizitie == 2011


def testCardClient():
    cardClient = CardClient(
        '2', 'Popescu', 'Andi', '1020817021919', '17.08.2002', '19.09.2021')
    assert cardClient.idEntitate == '2'
    assert cardClient.prenume == 'Andi'
    assert cardClient.dataNastere == '17.08.2002'


def testTranzactie():
    tranzactie = Tranzactie(
        '1', '1', 'None', 100, 250, '12.12.2020 10:15')
    assert tranzactie.idEntitate == '1'
    assert tranzactie.idCard == 'None'
    assert tranzactie.sumaPiese == 100

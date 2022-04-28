from Domain.masina import Masina
from Repository.repositoryJson import RepositoryJson
from Tests.utilFile import clearFile


def adaugareTest():
    clearFile("repositoryTest.txt")
    repository = RepositoryJson("repositoryTest.txt")

    masina = Masina('1', 'dacia', 2011, 100000, 'nu')

    repository.adauga(masina)
    masinaAdaugata = repository.getById('1')

    assert masinaAdaugata.model == 'dacia'
    assert masinaAdaugata.nrKm == 100000
    assert masinaAdaugata.inGarantie == 'nu'

    masina2 = Masina('2', 'renault', 2019, 50000, 'da')

    repository.adauga(masina2)
    masinaAdaugata2 = repository.getById('2')

    assert masinaAdaugata2.model == 'renault'
    assert masinaAdaugata2.anAchizitie == 2019
    assert masinaAdaugata2.inGarantie == 'da'


def stergereTest():
    clearFile("repositoryTest.txt")
    repository = RepositoryJson("repositoryTest.txt")

    masina = Masina('1', 'dacia', 2011, 100000, 'nu')
    masina2 = Masina('2', 'renault', 2019, 20500, 'da')

    repository.adauga(masina)
    repository.adauga(masina2)

    repository.sterge('1')
    masinaStearsa = repository.getById('1')
    masinaRamasa = repository.getById('2')

    assert masinaStearsa is None
    assert masinaRamasa.model == 'renault'
    assert masinaRamasa.nrKm == 20500

    repository.sterge('2')
    masinaStearsa = repository.getById('2')
    assert masinaStearsa is None


def modificaTest():
    clearFile("repositoryTest.txt")

    repository = RepositoryJson("repositoryTest.txt")

    masina = Masina('1', 'dacia', 2011, 100000, 'nu')
    masina2 = Masina('2', 'renault', 2019, 20500, 'da')

    repository.adauga(masina)
    repository.adauga(masina2)

    masina3 = Masina('1', 'audi', 2011, 120500, 'nu')
    repository.modifica(masina3)
    masinaModif = repository.getById('1')

    assert masinaModif is not None
    assert masinaModif.idEntitate == '1'
    assert masinaModif.anAchizitie == 2011
    assert masinaModif.inGarantie == 'nu'

    masina4 = Masina('2', 'renault', 2020, 100000, 'nu')
    repository.modifica(masina4)
    masinaModif2 = repository.getById('2')

    assert masinaModif2 is not None
    assert masinaModif2.idEntitate == '2'
    assert masinaModif2.anAchizitie == 2020
    assert masinaModif2.inGarantie == 'nu'
    assert masinaModif2.model == 'renault'

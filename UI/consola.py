from datetime import datetime

from Service.cardClientiService import CardClientService
from Service.masinaService import MasinaService
from Service.tranzactieService import TranzactieService
from Service.undoRedoService import UndoRedoService


class Consola:
    def __init__(self, masinaService: MasinaService,
                 cardClientService: CardClientService,
                 tranzactieService: TranzactieService,
                 undoRedoService: UndoRedoService):
        self.__masinaService = masinaService
        self.__cardClientService = cardClientService
        self.__tranzactieService = tranzactieService
        self.__undoRedoService = undoRedoService

    def runMenu(self) -> None:
        while True:
            print("1. CRUD masini")
            print("2. CRUD card client")
            print("3. CRUD trazactie")
            print("4. Cautare full text")
            print("5. Afișarea tuturor tranzacțiilor "
                  "cu suma cuprinsă într-un interval dat")
            print("6. Afișarea mașinilor ordonate "
                  "descrescător după suma obținută pe manoperă.")
            print("7. Afișarea cardurilor client ordonate "
                  "descrescător după valoarea reducerilor obținute.")
            print("8. Ștergerea tuturor tranzacțiilor "
                  "dintr-un anumit interval de zile.")
            print("9. Actualizarea garanției la fiecare mașină: "
                  "o mașină este în garanție dacă și numai "
                  "dacă are maxim 3 ani de la achiziție "
                  "și maxim 60 000 de km.")
            print("10. Stergere cascada")
            print("u. Undo")
            print("r. Redo")
            optiune = input("Dati optiune: ")

            if optiune == "1":
                self.runCRUDMasiniMenu()
            elif optiune == "2":
                self.runCRUDCardClientMenu()
            elif optiune == "3":
                self.runCRUDTranzactieMenu()
            elif optiune == "4":
                text = input("Da textul: ")
                self.uiCautareFullText(text)
            elif optiune == "5":
                self.uiTreanzactiiSumaInterval()
            elif optiune == "6":
                self.uiOrdonareMasiniDupaSuma()
            elif optiune == "7":
                self.uiOrdinareCarduriDupaReducere()
            elif optiune == "8":
                self.uiStrgereTranzactiiInterval()
            elif optiune == "9":
                self.uiActualizareGarantie()
            elif optiune == "10":
                self.uiStergereMasiniCascada()
            elif optiune == "u":
                self.__undoRedoService.undo()
            elif optiune == "r":
                self.__undoRedoService.redo()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati:")

    def runCRUDMasiniMenu(self) -> None:
        while True:
            print("1. Adauga masina")
            print("2. Sterge masina")
            print("3. Modifica masina")
            print("4.Generare masini")
            print("a. Afiseaza toate masinile")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.uiAdaugaMasina()
            elif optiune == "2":
                self.uiStergeMasina()
            elif optiune == "3":
                self.uiModificaMasina()
            elif optiune == "4":
                self.uiGenerareMasiniRandom()
            elif optiune == "a":
                self.showAllMasini()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati: ")

    def runCRUDCardClientMenu(self) -> None:
        while True:
            print("1. Adauga card client ")
            print("2. Sterge card client")
            print("3. Modifica card client")
            print("a. Afiseaza toate cardurile")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.uiAdaugaCardClient()
            elif optiune == "2":
                self.uiStergeCardClient()
            elif optiune == "3":
                self.uiModificaCardClient()
            elif optiune == "a":
                self.showAllCardClient()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati: ")

    def runCRUDTranzactieMenu(self) -> None:
        while True:
            print("1. Adauga tranzactie")
            print("2. Sterge tranzactie")
            print("3. Modifica tranzactie")
            print("a. Afiseaza toate tranzactiile")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.uiAdaugaTranzactie()
            elif optiune == "2":
                self.uiStergeTranzactie()
            elif optiune == "3":
                self.uiModificaTranzactie()
            elif optiune == "a":
                self.showAllTranzactii()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati: ")

    def uiAdaugaMasina(self) -> None:
        try:
            idMasina = input("Dati id-ul  masinii: ")
            model = input("Dati modelul masinii: ")
            anAchizitie = int(input("Dati anul anchizitiei"
                                    " masinii: "))
            nrKm = float(input("Dati numarul de km al masinii: "))
            inGarantie = input("Masina e in garantie(da/nu): ")

            self.__masinaService.adauga(
                idMasina, model, anAchizitie, nrKm, inGarantie)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiStergeMasina(self) -> None:
        try:
            idMasina = input(
                "Dati id-ul masinii de sters: ")

            self.__masinaService.sterge(idMasina)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiModificaMasina(self) -> None:
        try:
            idMasina = input("Dati id-ul  masinii: ")
            model = input("Dati modelul masinii: ")
            anAchizitie = int(input(
                "Dati anul anchizitiei masinii: "))
            nrKm = float(input("Dati numarul de km al masinii: "))
            inGarantie = input("Masina e in garantie(da/nu): ")

            self.__masinaService.modifica(
                idMasina, model, anAchizitie, nrKm, inGarantie)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def showAllMasini(self) -> None:
        for masina in self.__masinaService.getAll():
            print(masina)

    def uiAdaugaCardClient(self) -> None:
        try:
            idCard = input("Dati id-ul cardului: ")
            nume = input("Dati numele clientului: ")
            prenume = input("Dati prenumele clientului: ")
            cnp = input("Dati CNP-ul: ")
            dataNastere = input("Dati data nasterii(DD.MM.YYYY): ")
            dataInreg = input("Dati data inregistrarii(DD.MM.YYYY): ")

            self.__cardClientService.adauga(
                idCard, nume, prenume, cnp, dataNastere, dataInreg
            )
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiStergeCardClient(self) -> None:
        try:
            idCard = input("Dati id-ul cardului: ")

            self.__cardClientService.sterge(idCard)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiModificaCardClient(self) -> None:
        try:
            idCard = input("Dati id-ul cardului: ")
            nume = input("Dati numele clientului: ")
            prenume = input("Dati prenumele clientului: ")
            cnp = input("Dati CNP-ul: ")
            dataNastere = input("Dati data nasterii(DD.MM.YYYY): ")
            dataInreg = input("Dati data inregistrarii(DD.MM.YYYY): ")

            self.__cardClientService.modifica(
                idCard, nume, prenume, cnp, dataNastere, dataInreg
            )
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def showAllCardClient(self) -> None:
        for card in self.__cardClientService.getAll():
            print(card)

    def uiAdaugaTranzactie(self) -> None:
        try:
            idTranzactie = input("Dati id-ul tranzactiei: ")
            idMasina = input("Dati id-ul masinii: ")
            idCard = input("Dati id-ul cardului "
                           "sau None daca nu exista: ")
            sumaPiese = float(input("Dati suma pieselor: "))
            manopera = float(input("Dati valoarea manoperei: "))
            dataOra = input("Dati data si ora( DD.MM.YYYY H:M): ")

            self.__tranzactieService.adauga(
                idTranzactie, idMasina, idCard, sumaPiese, manopera, dataOra
            )
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiStergeTranzactie(self) -> None:
        try:
            idTranzactie = input("Dati id-ul tranzactiei: ")

            self.__tranzactieService.sterge(idTranzactie)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiModificaTranzactie(self) -> None:
        try:
            idTranzactie = input("Dati id-ul tranzactiei: ")
            idMasina = input("Dati id-ul masinii: ")
            idCard = input("Dati id-ul cardului "
                           "sau None daca nu exista: ")
            sumaPiese = float(input("Dati suma pieselor: "))
            manopera = float(input("Dati valoarea manoperei: "))
            dataOra = input("Dati data si ora( DD.MM.YYYY H:M): ")

            self.__tranzactieService.modifica(
                idTranzactie, idMasina, idCard, sumaPiese, manopera, dataOra
            )
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def showAllTranzactii(self) -> None:
        for tranzactie in self.__tranzactieService.getAll():
            print(tranzactie)

    def uiGenerareMasiniRandom(self) -> None:
        n = int(input("Da nr. de masini: "))
        self.__masinaService.generareMasiniRandom(n)

    def uiCautareFullText(self, text) -> None:
        lista = []
        listaMasini = \
            self.__masinaService.cautareFullTextMasini(text)
        listaClienti = \
            self.__cardClientService.cautareFullTextClienti(text)
        if len(listaMasini) > 0:
            lista.append(listaMasini)
        if len(listaClienti) > 0:
            lista.append(listaClienti)
        print(lista)

    def uiTreanzactiiSumaInterval(self) -> None:
        try:
            suma1 = float(input("Da primul "
                                "capat de interval: "))
            suma2 = float(input("Da al "
                                "doilea capat de inerval: "))
            tranzactii = self.__tranzactieService.getAll()
            rezultat = []
            print(
                self.__tranzactieService.treanzactiiSumaInterval(suma1, suma2,
                                                                 tranzactii,
                                                                 rezultat))
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiStrgereTranzactiiInterval(self):
        try:
            data1 = input("Da primul capat de interval: ")
            data2 = input("Da al doilea capat de inerval: ")
            datetime.strptime(data1, '%d.%m.%Y %H:%M')
            datetime.strptime(data2, '%d.%m.%Y %H:%M')
            self.__tranzactieService.strgereTranzactiiInterval(data1, data2)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiActualizareGarantie(self):
        self.__masinaService.actualizareGarantie()

    def uiOrdonareMasiniDupaSuma(self):
        for masina in self.__tranzactieService.ordoneazaMasiniDupaSuma():
            print(masina)

    def uiOrdinareCarduriDupaReducere(self):
        for card in self.__tranzactieService.ordoneazaCarduriDupaReducere():
            print(card)

    def uiStergereMasiniCascada(self):
        idMasina = input("Da id-ul masinii de sters in cascada: ")
        self.__tranzactieService.stergereMasiniCascada(idMasina)

from Domain.undoRedoOperation import UndoRedoOperation
from Repository.repository import Repository


class MultiDeleteCascada(UndoRedoOperation):
    def __init__(self, repository1: Repository,
                 repository2: Repository,
                 obiecteSterse: list,
                 obiectesterse2: list):
        self.__repository1 = repository1
        self.__repository2 = repository2
        self.__obiecteSterse = obiecteSterse
        self.__obiectesterse2 = obiectesterse2

    def doUndo(self):
        for entitate in self.__obiecteSterse:
            self.__repository1.adauga(entitate)
        for entitate2 in self.__obiectesterse2:
            self.__repository2.adauga(entitate2)

    def doRedo(self):
        for entitate in self.__obiecteSterse:
            self.__repository1.sterge(entitate.idEntitate)
        for entitate2 in self.__obiectesterse2:
            self.__repository2.sterge(entitate2.idEntitate)

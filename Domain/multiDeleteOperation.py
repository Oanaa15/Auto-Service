from Domain.undoRedoOperation import UndoRedoOperation
from Repository.repository import Repository


class MultiDelete(UndoRedoOperation):
    def __init__(self, repository: Repository,
                 obiecte: list):
        self.__repository = repository
        self.__obiecte = obiecte

    def doUndo(self):
        for entitate in self.__obiecte:
            self.__repository.adauga(entitate)

    def doRedo(self):
        for entitate in self.__obiecte:
            self.__repository.sterge(entitate.idEntitate)

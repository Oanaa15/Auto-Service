from Domain.undoRedoOperation import UndoRedoOperation


class UndoRedoService:
    def __init__(self):
        self.__undoOperations = []
        self.__redoOperations = []

    def addUndoRedoOperation(self, undoRedoOperation: UndoRedoOperation):
        self.__undoOperations.append(undoRedoOperation)
        self.__redoOperations.clear()

    def undo(self):
        try:
            if self.__undoOperations:
                undoOperation = self.__undoOperations.pop()
                self.__redoOperations.append(undoOperation)
                undoOperation.doUndo()
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def redo(self):
        try:
            if self.__redoOperations:
                redoOperation = self.__redoOperations.pop()
                self.__undoOperations.append(redoOperation)
                redoOperation.doRedo()
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

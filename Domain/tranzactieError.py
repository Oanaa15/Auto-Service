from dataclasses import dataclass


@dataclass
class TranzactieError(Exception):
    mesaj: any

    def __str__(self) -> str:
        return f'TranzactieError: {self.mesaj}'

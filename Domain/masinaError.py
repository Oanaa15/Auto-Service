from dataclasses import dataclass


@dataclass
class MasinaError(Exception):
    mesaj: any

    def __str__(self) -> str:
        return f'MasinaError: {self.mesaj}'

from dataclasses import dataclass


@dataclass
class Regista:
    name_id: str
    name: str

    def __hash__(self):
        return hash(self.name_id)

    def __eq__(self,other):
        return self.name_id == other.name_id

    def __str__(self):
        return f'{self.name}'
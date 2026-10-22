from dataclasses import dataclass

from model.regista import Regista


@dataclass
class Arco:
    r1: Regista
    r2: Regista
    peso: int

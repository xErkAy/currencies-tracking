from dataclasses import dataclass


@dataclass
class CurrencyInstance:
    id: str
    num_code: str
    char_code: str
    name: str
    value: float
    nominal: int

    def __init__(self, data: dict):
        self.id = data.get('ID')
        self.num_code = data.get('NumCode')
        self.char_code = data.get('CharCode')
        self.name = data.get('Name')
        self.value = data.get('Value')
        self.nominal = data.get('Nominal')

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
        self.id = data['ID']
        self.num_code = data['NumCode']
        self.char_code = data['CharCode']
        self.name = data['Name']
        self.value = data['Value']
        self.nominal = data['Nominal']

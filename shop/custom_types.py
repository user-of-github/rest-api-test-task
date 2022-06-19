import dataclasses

SHOP_UNIT_TYPES: tuple = (('CATEGORY', 'CATEGORY'), ('OFFER', 'OFFER'))


@dataclasses.dataclass
class Error:
    code: int
    message: str

    def to_dict(self):
        return {'code': self.code, 'message': self.message}
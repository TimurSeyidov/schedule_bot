from typing import List
from src.classes import Group

fake_data = [
    Group(id=1, name='ИБ-22', year=2023),
    Group(id=2, name='ПИ-31', year=2024),
    Group(id=3, name='М-11', year=2023),
    Group(id=4, name='ИБ-43', year=2025),
    Group(id=5, name='ПИ-13', year=2024),
    Group(id=6, name='М-12', year=2023),
    Group(id=7, name='ПИ-21', year=2023),
    Group(id=8, name='ИБ-42', year=2025),
    Group(id=9, name='М-32', year=2024),
    Group(id=10, name='ПИ-11', year=2023),
    Group(id=11, name='ИБ-31', year=2024),
    Group(id=12, name='ПИ-41', year=2025),
    Group(id=13, name='М-21', year=2023),
    Group(id=14, name='ИБ-23', year=2024),
    Group(id=15, name='ПИ-12', year=2023),
    Group(id=16, name='М-43', year=2025),
    Group(id=17, name='ИБ-11', year=2023),
    Group(id=18, name='ПИ-33', year=2024),
    Group(id=19, name='М-22', year=2023),
    Group(id=20, name='ИБ-12', year=2023),
    Group(id=21, name='ПИ-42', year=2025),
    Group(id=22, name='М-13', year=2023),
    Group(id=23, name='ИБ-33', year=2024),
    Group(id=24, name='ПИ-22', year=2023),
    Group(id=25, name='М-41', year=2025),
    Group(id=26, name='ИБ-13', year=2023),
    Group(id=27, name='ПИ-23', year=2023),
    Group(id=28, name='М-23', year=2023),
    Group(id=29, name='ИБ-21', year=2025),
    Group(id=30, name='ПИ-32', year=2024),
]

class Groups:
    @staticmethod
    def all() -> List[Group]:
        return fake_data[::]

    @staticmethod
    def get_by_id(_id: int) -> Group | None:
        result = list(filter(lambda g: g.id == _id, fake_data))
        return result[0] if result else None

    @staticmethod
    def get_by_ids(_ids: List[int]) -> List[Group]:
        return list(filter(lambda g: g.id in _ids, fake_data))
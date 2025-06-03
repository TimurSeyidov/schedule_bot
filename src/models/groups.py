from typing import List, Type
from sqlalchemy.orm import Session
from src.dao import Group


fake_data = [
    Group(name='ИБ-22', year=2023),
    Group(name='ПИ-31', year=2024),
    Group(name='М-11', year=2023),
    Group(name='ИБ-43', year=2025),
    Group(name='ПИ-13', year=2024),
    Group(name='М-12', year=2023),
    Group(name='ПИ-21', year=2023),
    Group(name='ИБ-42', year=2025),
    Group(name='М-32', year=2024),
    Group(name='ПИ-11', year=2023),
    Group(name='ИБ-31', year=2024),
    Group(name='ПИ-41', year=2025),
    Group(name='М-21', year=2023),
    Group(name='ИБ-23', year=2024),
    Group(name='ПИ-12', year=2023),
    Group(name='М-43', year=2025),
    Group(name='ИБ-11', year=2023),
    Group(name='ПИ-33', year=2024),
    Group(name='М-22', year=2023),
    Group(name='ИБ-12', year=2023),
    Group(name='ПИ-42', year=2025),
    Group(name='М-13', year=2023),
    Group(name='ИБ-33', year=2024),
    Group(name='ПИ-22', year=2023),
    Group(name='М-41', year=2025),
    Group(name='ИБ-13', year=2023),
    Group(name='ПИ-23', year=2023),
    Group(name='М-23', year=2023),
    Group(name='ИБ-21', year=2025),
    Group(name='ПИ-32', year=2024),
]

class Groups:
    @staticmethod
    def load_fake_data(session: Session):
        for data in fake_data:
            session.add(data)
        session.commit()

    @staticmethod
    def all(session: Session) -> List[Type[Group]]:
        return (session
                .query(Group)
                .order_by(*[
                    Group.year,
                    Group.name
                ]).all())

    @staticmethod
    def get_by_id(session: Session, _id: int) -> Type[Group] | None:
        return (session
                .query(Group)
                .filter(Group.id == _id)
                .first())

    @staticmethod
    def get_by_ids(session: Session, _ids: List[int]) -> List[Type[Group]]:
        return (session
                .query(Group)
                .filter(Group.id.in_(_ids))
                .order_by(*[
                    Group.year,
                    Group.name
                ])
                .all())

from sqlalchemy import Column, Integer, String, UniqueConstraint
from .base import Base

class Group(Base):
    """Модель группы"""
    __tablename__: str = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    year = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(*['name', 'year'], name='uniq_name_year_1'),
    )

    def __repr__(self) -> str:
        return 'Group(id={}, name="{}", year={}'.format(*[
            self.id,
            self.name,
            self.year
        ])
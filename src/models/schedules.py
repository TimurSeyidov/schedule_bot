from typing import List
from src.classes import Schedule

fake_data = [
    Schedule(id=1, group_id=29, date='2025-05-29', position=1, name='Математика', description='Иванов'),
    Schedule(id=2, group_id=29, date='2025-05-29', position=2, name='Физика', description='Петров'),
    Schedule(id=3, group_id=29, date='2025-05-29', position=3, name='Информатика', description='Сидоров'),
    Schedule(id=4, group_id=29, date='2025-05-29', position=4, name='История', description='Кузнецов'),
    Schedule(id=5, group_id=29, date='2025-05-29', position=5, name='Литература', description='Смирнов'),
    Schedule(id=6, group_id=29, date='2025-05-29', position=6, name='Биология', description='Васильев'),
    Schedule(id=7, group_id=29, date='2025-05-30', position=1, name='Химия', description='Попов'),
    Schedule(id=8, group_id=29, date='2025-05-30', position=2, name='География', description='Соколов'),
    Schedule(id=9, group_id=29, date='2025-05-30', position=3, name='Математика', description='Иванов'),
    Schedule(id=10, group_id=29, date='2025-05-30', position=4, name='Физика', description='Петров'),
    Schedule(id=11, group_id=29, date='2025-05-30', position=5, name='Информатика', description='Сидоров'),
    Schedule(id=12, group_id=29, date='2025-05-30', position=6, name='История', description='Кузнецов'),
    Schedule(id=13, group_id=29, date='2025-05-31', position=1, name='Литература', description='Смирнов'),
    Schedule(id=14, group_id=29, date='2025-05-31', position=2, name='Биология', description='Васильев'),
    Schedule(id=15, group_id=29, date='2025-05-31', position=3, name='Химия', description='Попов'),
    Schedule(id=16, group_id=29, date='2025-05-31', position=4, name='География', description='Соколов'),
    Schedule(id=17, group_id=29, date='2025-05-31', position=5, name='Математика', description='Иванов'),
    Schedule(id=18, group_id=29, date='2025-05-31', position=6, name='Физика', description='Петров'),
    Schedule(id=19, group_id=29, date='2025-06-01', position=1, name='Информатика', description='Сидоров'),
    Schedule(id=20, group_id=29, date='2025-06-01', position=2, name='История', description='Кузнецов'),
    Schedule(id=21, group_id=29, date='2025-06-01', position=3, name='Литература', description='Смирнов'),
    Schedule(id=22, group_id=29, date='2025-06-01', position=4, name='Биология', description='Васильев'),
    Schedule(id=23, group_id=29, date='2025-06-01', position=5, name='Химия', description='Попов'),
    Schedule(id=24, group_id=29, date='2025-06-01', position=6, name='География', description='Соколов'),
    Schedule(id=25, group_id=29, date='2025-06-02', position=1, name='Математика', description='Иванов'),
    Schedule(id=26, group_id=29, date='2025-06-02', position=2, name='Физика', description='Петров'),
    Schedule(id=27, group_id=29, date='2025-06-02', position=3, name='Информатика', description='Сидоров'),
    Schedule(id=28, group_id=29, date='2025-06-02', position=4, name='История', description='Кузнецов'),
    Schedule(id=29, group_id=29, date='2025-06-02', position=5, name='Литература', description='Смирнов'),
    Schedule(id=30, group_id=29, date='2025-06-02', position=6, name='Биология', description='Васильев'),
    Schedule(id=31, group_id=29, date='2025-06-03', position=1, name='Химия', description='Попов'),
    Schedule(id=32, group_id=29, date='2025-06-03', position=2, name='География', description='Соколов'),
    Schedule(id=33, group_id=29, date='2025-06-03', position=3, name='Математика', description='Иванов'),
    Schedule(id=34, group_id=29, date='2025-06-03', position=4, name='Физика', description='Петров'),
    Schedule(id=35, group_id=29, date='2025-06-03', position=5, name='Информатика', description='Сидоров'),
    Schedule(id=36, group_id=29, date='2025-06-03', position=6, name='История', description='Кузнецов'),
    Schedule(id=37, group_id=29, date='2025-06-04', position=1, name='Литература', description='Смирнов'),
    Schedule(id=38, group_id=29, date='2025-06-04', position=2, name='Биология', description='Васильев'),
    Schedule(id=39, group_id=29, date='2025-06-04', position=3, name='Химия', description='Попов'),
    Schedule(id=40, group_id=29, date='2025-06-04', position=4, name='География', description='Соколов')
]

class Schedules:
    @staticmethod
    def get_items_by_group_id(_id: int) -> List[Schedule]:
        print(_id)
        return list(filter(lambda s: s.group_id == _id, fake_data))

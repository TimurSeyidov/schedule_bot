from typing import Dict, List, Tuple
from ..classes import SubscriptionType, Subscribe, Group

fake_data = {
    '179844404': [
        Subscribe(
            id=1,
            outer_id=29,
            type=SubscriptionType.GROUP,
            user_id='7813309501',
            name='ИБ-21'
        ),
        # Subscribe(id=2, type=SubscriptionType.TEACHER, name='Сейидов Т.Т.', user_id='7813309501'),
    ],
    '2140610926': [
        Subscribe(
            id=3,
            outer_id=29,
            type=SubscriptionType.GROUP,
            user_id='2140610926',
            name='ИБ-21'
        ),
    ],
    '1084483214': [
        Subscribe(
            id=4,
            outer_id=29,
            type=SubscriptionType.GROUP,
            user_id='1084483214',
            name='ИБ-21'
        ),
    ]
}

class Settings:
    @staticmethod
    def get_subscribe_by_user_id(user_id: str | int) -> List[Subscribe]:
        return sorted(
            fake_data.get(str(user_id), []),
            key=lambda item: (0 if item.type == SubscriptionType.GROUP else 1, item.name)
        )

    @staticmethod
    def get_subscribe_by_id(_id: int, user_id) -> Subscribe | None:
        subscribes = list(filter(lambda s: s.id == _id, fake_data.get(str(user_id), [])))
        return subscribes[0] if subscribes else None
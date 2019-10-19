from typing import Dict
import uuid
from dataclasses import dataclass, field
from models.item import Item
from models.model import Model
from models.user import User
from libs.mailgun import Mailgun


@dataclass(eq=False)
class Alert(Model):
    collection: str = field(init=False, default='alerts')
    name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            'name': self.name,
            'item_id': self.item_id,
            'price_limit': self.price_limit,
            'user_email': self.user_email,
            '_id': self._id
        }

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):
        if self.item.price < self.price_limit:
            print(
                f'Item {self.item} has reached {self.item.price} in price, and is now below {self.price_limit}.')
            Mailgun.send_mail(
                ['lentmiien@gmail.com'],
                f'Notification for {self.name}',
                f'Your alert {self.name} has reached a price under {self.price_limit}. The latest price is {self.item.price}. Go to the address to check your item: {self.item.url}',
                f'<p>Your alert {self.name} has reached a price under {self.price_limit}.</p><p>The latest price is {self.item.price}.</p><p>Click <a href="{self.item.url}">here</a> to purchase your item.</p>'
                )

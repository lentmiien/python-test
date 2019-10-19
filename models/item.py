from typing import Dict
from dataclasses import dataclass, field
import uuid
import re
import requests
from bs4 import BeautifulSoup
from models.model import Model


@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default='items')
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def load_price(self) -> float:
        if self.price is None:
            response = requests.get(self.url)
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')
            element = soup.find(self.tag_name, self.query)
            string_price = element.text.strip()

            pattern = re.compile(r'(\d+,?\d*\.\d\d)')
            match = pattern.search(string_price)
            found_price = match.group(1)
            whitout_commas = found_price.replace(',', '')
            self.price = float(whitout_commas)
        return self.price

    def json(self) -> Dict:
        return {
            'url': self.url,
            'tag_name': self.tag_name,
            'query': self.query,
            'price': self.price,
            '_id': self._id
        }

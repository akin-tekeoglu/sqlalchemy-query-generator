import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from tests.model import Base, User, Adress
from sqlalchemy_query_helper.query_generator import generate_query

engine = create_engine("sqlite:///:memory:", echo=True)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()
ed_user1 = User(
    name="ed",
    fullname="Ed Jones",
    nickname="edsnickname",
    timestamp=datetime.datetime.utcnow() - datetime.timedelta(days=1),
)
ad = Adress(title="title", description="description")
ad1 = Adress(title="title1", description="description")
ed_user1.addresses.append(ad)
ed_user1.addresses.append(ad1)
session.add(ed_user1)
session.commit()
q = generate_query(
    session,
    User,
    {
        "or": [
            {"fullname": {"op": "eq", "value": "Ed Jones"}},
            {"fullname": {"op": "eq", "value": "ed"}},
            {
                "and": [
                    {
                        "addresses": {
                            "foos": {"bars": {"bar": {"op": "eq", "value": "title"}}}
                        }
                    },
                    {"addresses": {"foos": {"foo": {"op": "eq", "value": "title"}}},},
                ],
            },
        ],
        "timestamp": {"op": "gte", "value": "2020-05-04T00:05:23"},
    },
)
print(list(q)[0].addresses)


import dateparser
from datetime import datetime, date
from dataclasses import dataclass
from datamodels import Model


@dataclass
class Person(Model):
    name: str
    title: str = None
    birthdate: date = None

    class CONVERTERS:
        def birthdate(value):
            return (
                dateparser.parse(value).date()
                if not isinstance(value, (datetime, date))
                else value
            )

    class VALIDATORS:
        def title(instance, field, value):
            print(instance, field, value)
            values = {'Mr', 'Ms', 'Mrs', 'Dr'}
            if value is not None and value not in values:
                raise ValueError(f'{field} must be one of {values}.')

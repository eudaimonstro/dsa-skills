import re
import sqlalchemy as sa
from typing import List, Dict, Any

from sqlalchemy.dialects.sqlite import DATE
from sqlalchemy import desc, asc

from db import db

custom_date_type = DATE(storage_format='%(month)d/%(day)d/%(year)04d',
                        regexp=re.compile('(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+)'))


class MemberModel(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    profile_image = db.Column(db.UnicodeText)
    dues_paid = db.Column(db.Boolean)
    last_dues_payment = db.Column(custom_date_type)
    chapter_name = db.Column(db.String)

    def __init__(self, first_name, last_name, email, profile_image, dues_paid, last_dues_payment, chapter_name):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.profile_image = profile_image
        self.dues_paid = dues_paid
        self.last_dues_payment = last_dues_payment
        self.chapter_name = chapter_name

    def __repr__(self):
        return self._repr(first_name=self.first_name,
                          last_name=self.last_name,
                          email=self.email,
                          profile_image=self.profile_image,
                          dues_paid=self.dues_paid,
                          last_dues_payment=self.last_dues_payment,
                          chapter_name=self.chapter_name)

    def json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'profile_image': self.profile_image,
            'dues_paid': self.dues_paid,
            'last_dues_payment': f'{self.last_dues_payment.month}/{self.last_dues_payment.day}/{self.last_dues_payment.year}',
            'chapter_name': self.chapter_name
        }

    @ classmethod
    def find_by_id(cls, _id) -> 'MemberModel':
        return cls.query.filter_by(id=_id).first()

    @ classmethod
    def find_all(cls, sort=False, invert=False) -> List['MemberModel']:
        if sort:
            if sort == 'first_name':
                if invert:
                    return cls.query.order_by(desc(MemberModel.first_name)).all()
                else:
                    return cls.query.order_by(asc(MemberModel.first_name)).all()
            elif sort == 'last_name':
                if invert:
                    return cls.query.order_by(desc(MemberModel.last_name)).all()
                else:
                    return cls.query.order_by(asc(MemberModel.last_name)).all()
        else:
            return cls.query.all()

    @ classmethod
    def find_by_chapter(cls, chapter_name) -> List['MemberModel']:
        return cls.query.filter(cls.chapter_name.like(f'%{chapter_name}%'))

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def _repr(self, **fields: Dict[str, Any]) -> str:
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f"{key}={field!r}")
            except sa.orm.exc.DetachedInstanceError:
                field_strings.append(f"{key}=DetachedInstanceError")
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({', '.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

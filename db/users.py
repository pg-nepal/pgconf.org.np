import sqlalchemy as sa
from passlib.hash import bcrypt
import db


class Users(db.Base):
    __tablename__  = 'users'
    __table_args__ = {
        'schema'  : 'conf25',
        'comment' : 'conference proposals',
    }

    pk             = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    username       = sa.Column(sa.String(256), nullable=False, unique=True)
    email          = sa.Column(sa.String(256), nullable=False, unique=True)
    password       = sa.Column(sa.String(60), nullable=True)
    createdOn      = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())  # noqa:E501

    def set_password(self, password):
        self.password = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password)
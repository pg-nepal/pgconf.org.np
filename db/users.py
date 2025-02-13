import os
import hashlib

import sqlalchemy as sa
import db


class Users(db.Base):
    __tablename__  = 'users'
    __table_args__ = {
        'schema'  : 'um',
        'comment' : 'users list',
    }

    pk             = sa.Column(sa.Integer, autoincrement=True, primary_key=True) # noqa: E501

    # https        ://en.wikipedia.org/wiki/Salt_(cryptography)
    salt           = sa.Column(sa.dialects.postgresql.BYTEA)
    hashed         = sa.Column(sa.dialects.postgresql.BYTEA)
    uname          = sa.Column(sa.String(32), nullable=False, unique=True)

    fullname       = sa.Column(sa.String(256))
    email          = sa.Column(sa.String(256), index=True, unique=True)
    mobile         = sa.Column(sa.String(15), index=True, unique=True)

    ##
    def set_password(self, shadow):
        salt = os.urandom(16)
        hashed = hashlib.scrypt(
            password = shadow.encode('utf-8'),  # in octet string
            salt     = salt,  # in octet string
            r        = 8,  # block size
            n        = 1024,  # CPU/Memory cost, range: 1 < n < 2^(128 * r / 8) # noqa: E501
            p        = 1,  # parallelization factor
            maxmem   = 32 * 1024 * 1024,  # limits memory
            dklen    = 64,  # output (derived key) length default:64
        )

        self.salt = salt
        self.password = hashed

    ##
    def check_password(self, password):
        hashed_attempt = hashlib.scrypt(
        password = password.encode('utf-8'),  # in octet string
        salt     = self.salt,  # in octet string
        r        = 8,  # block size
        n        = 1024,  # CPU/Memory cost, range: 1 < n < 2^(128 * r / 8)
        p        = 1,  # parallelization factor
        maxmem   = 32 * 1024 * 1024,  # limits memory
        dklen    = 64,  # output (derived key) length default:64
        )
        return hashed_attempt == self.hashed

    def assign_creator(self, createdBy):
        self.createdBy = createdBy

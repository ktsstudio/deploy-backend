from server.store.gino import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(32), nullable=False)


class Session(db.Model):
    __tablename__ = "session"
    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(64), nullable=False)

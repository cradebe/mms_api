from sqlalchemy import DateTime

from resources.database.conf import db


class Image(db.Model):
    __tablename__ = 'image'

    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_path = db.Column(db.String, nullable=False)
    image_name = db.Column(db.String, nullable=False)
    image_mimetype = db.Column(db.String, nullable=False)
    date_created = db.Column(DateTime, server_default=db.func.now(), nullable=False)

    def __init__(self, path, name, mimetype):
        self.image_name = name
        self.image_mimetype = mimetype
        self.image_path = path

    def json(self):
        return {'imageTimestamp': self.date_created, 'imageName': self.image_name, 'imageURL': self.image_path}

import json
import os
from datetime import datetime
from typing import List

from flask import Flask, request, jsonify
from sqlalchemy import inspect
from werkzeug import Response
from werkzeug.utils import secure_filename

from resources.database.conf import db, app
from resources.database.models import Image


@app.route('/')
def get_all_images() -> Response or (str, int):
    images: List[Image] = Image.query.order_by(Image.date_created).all()
    if not images:
        return 'Image Not Found!', 404
    response_images = []
    for img in images:
        response_dict = {}
        data_dict = inspect(img).dict
        del data_dict['_sa_instance_state']
        response_dict['imageId'] = data_dict['image_id']
        response_dict['imageTimestamp'] = data_dict['date_created']
        response_dict['imageUrl'] = data_dict['image_path']
        response_dict['imageName'] = data_dict['image_name']

        response_images.append(response_dict)
    return response_images


@app.route('/<int:id>')
def get_image(image_id: int) -> Response or (str, int):
    img = Image.query.filter_by(id=image_id).first()
    if not img:
        return 'Image Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)


@app.route('/upload', methods=['POST'])
def upload() -> (str, int):
    image = request.files['image']
    if not image:
        return Response('No picture uploaded!', 400)
    filename = secure_filename(image.filename)
    mimetype = image.mimetype
    extension = mimetype.split('/')[1]
    if not filename or not mimetype:
        return Response('Unable to upload!', 400)
    image_data = image.read()
    path = save_image(image_data, filename, extension)
    img = Image(path=path, name=filename, mimetype=mimetype)
    db.session.add(img)

    db.session.flush()
    data_dict = inspect(img).dict
    response_dict = {'imageId': data_dict['image_id'],
                     'imageUrl': data_dict['image_path'],
                     'imageName': data_dict['image_name']}

    db.session.commit()
    img: Image = db.session().query(Image).filter(response_dict['imageId'] == Image.image_id).first()
    response_dict['imageTimestamp'] = img.date_created
    return response_dict


def save_image(image_data, file_name: str, extension: str) -> str:
    full_file_name = f'{file_name}_{datetime.now().strftime("%m-%d-%Y")}.{extension}'
    save_path = f'{os.environ.get("image_path")}{full_file_name}'
    full_path = f'assets/images/{full_file_name}'
    with open(save_path, 'wb') as file:
        file.write(image_data)
    return full_path


if __name__ == '__main__':
    app.run()

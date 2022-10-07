import json
import os
from datetime import datetime
from typing import List

from flask import request, Response
from werkzeug.utils import secure_filename

from resources.database.conf import db, app
from resources.database.models import Image


# region end points
@app.route('/')
def get_all_images() -> (dict, int):

    """
     Description:
     ------------
         This method retrieves all images from a database

     Parameters:
     ----------
         None

     Returns:
     -------
         Image Data List: this is a list of dictionaries containing image data

         Status Code: This is an integer containing the request status code
     """
    # get list of images
    images: List[Image] = db.session().query(Image).order_by(Image.date_created).all()

    if not images:
        return Response('Image Not Found!', 404)

    response_images = []

    for img in images:
        response_images.append(img.json())

    return response_images, 200


@app.route('/delete/<int:id>')
def delete_image(image_id: int) -> Response:

    """
    Description:
    ------------
        This method retrieves a single image from the database and removes it

    Parameters:
    ----------
        image_id: and integer containing the id of the image to be retrieved

    Returns:
    -------
        Response: This is a flask object containing response message and status code
    """

    img: Image = db.session().query(Image).filter(Image.image_id == image_id).first()

    if not img:
        return Response('Image Not Found!', 404)
    db.session().delete(img)
    db.session().commit()

    return Response(f"{img.image_name} has been deleted")


@app.route('/<int:id>')
def get_image(image_id: int) -> (dict, int):

    """
    Description:
    ------------
        This method retrieves a single image from the database

    Parameters:
    ----------
        image_id: and integer containing the id of the image to be retrieved

    Returns:
    -------
        Image Data: this is a dictionary containing image data

        Status Code: This is an integer containing the request status code
    """

    img = db.session().query(Image).filter(Image.image_id == image_id).first()

    if not img:
        return 'Image Not Found!', 404

    return img.json(), 200


@app.route('/upload', methods=['POST'])
def upload() -> (dict, int):

    """
    Description:
    ------------
        This method imports data from client request to database and returns the single uploaded image data

    Parameters:
    ----------
        None

    Returns:
    -------
        Image Data: this is a dictionary containing image data

        Status Code: This is an integer containing the request status code
    """

    # get image data from request object
    image = request.files['image']

    if not image:
        return Response('No picture uploaded!', 400)

    filename = secure_filename(image.filename)
    mimetype = image.mimetype
    extension = mimetype.split('/')[1]

    if not filename or not mimetype:
        return Response('Unable to upload!', 400)

    image_data = image.read()
    # save image to folder
    path = save_image(image_data, filename, extension)

    # create image object
    img = Image(path=path, name=filename, mimetype=mimetype)

    db.session.add(img)
    # this hydrates/populates the image id
    db.session.flush()
    # this will ensure that time stamp data is populated
    db.session.refresh(img)

    db.session.commit()

    return img.json(), 200


# endregion

# region Helper
def save_image(image_data: bytes, file_name: str, extension: str) -> str:

    """
     Description:
     ------------
         This method saves the image data in memory to a designated folder

     Parameters:
     ----------
         image_data: image data in byte format

         file_name: a string containing the file name

         extension: a string containing the file extension

     Returns:
     -------
         Image Data: this is a dictionary containing image data

         Status Code: This is an integer containing the request status code
     """
    
    # full path on the server
    full_file_name = f'{file_name}_{datetime.now().strftime("%m-%d-%Y")}.{extension}'
    save_path = f'{os.environ.get("image_path")}{full_file_name}'
    # angular path
    full_path = f'assets/images/{full_file_name}'

    with open(save_path, 'wb') as file:
        file.write(image_data)
    return full_path


# endregion
if __name__ == '__main__':
    app.run()

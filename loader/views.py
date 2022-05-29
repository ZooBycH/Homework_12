import random

from flask import render_template, Blueprint, request, current_app
import os
from classes.data_manager import DataManager
from .exceptions import OutOffFreeNamesError, PictureFormatNotSupported, PictureNotUploadedError
from .upload_manager import UploadManager

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')


@loader_blueprint.route('/post', methods=['GET'])
def page_form():
    return render_template('post_form.html')


@loader_blueprint.route('/post', methods=['POST'])
def page_create_posts():
    path = current_app.config.get("POST_PATH")
    dm = DataManager(path)
    upload_manager = UploadManager()

    # Получаем данные
    picture = request.files.get('picture', None)
    content = request.values.get('content', '')

    # Сохраняем картинку с помощью  менеджера загрузок
    filename = upload_manager.save_picture(picture)

    web_path = f"/uploads/images/{filename}"

    # данные для записи в файл
    post = {"pic": web_path, "content": content}

    dm.add(post)

    return render_template('post_uploaded.html', pic=web_path, content=content)


@loader_blueprint.errorhandler(OutOffFreeNamesError)
def error_out_of_free_name(e):
    return "Закончились свободные имена для загрузки картинок"


@loader_blueprint.errorhandler(PictureFormatNotSupported)
def error_format_supported(e):
    return "Формат картинки не поддерживается"


@loader_blueprint.errorhandler(PictureNotUploadedError)
def error_upload(e):
    return "Не удалось загрузить картинку"

import logging
import os

from loader.exceptions import PictureFormatNotSupported, PictureNotUploadedError


class UploadManager:

    def is_file_type_valid(self, file_type):
        if file_type.lower() in ["jpg", "jpeg", "png", "gif"]:
            return True
        return False

    def save_picture(self, picture):
        # Получаем данные картинки

        filename = picture.filename
        file_type = filename.split('.')[-1]
        folder = os.path.join(".", "uploads", "images")

        # Проверяем валидность картинок
        logger = logging.getLogger('basic')
        if not self.is_file_type_valid(file_type):
            logger.info(f"загруженный файл - не картинка")
            raise PictureFormatNotSupported(f"Формат {file_type} не поддерживается")

        # Создаем случайное название изображению
        # filename_to_save = get_free_filename(folder, file_type)

        # Сохраняем
        try:
            picture.save(os.path.join(folder, filename))
        except FileNotFoundError:
            logger.error("файл не загружен")
            raise PictureNotUploadedError(f"{folder, filename}")

        return filename

# def get_free_filename(folder, file_type):
#     """Возвращает случайное имя загруженной картинке из заданного диапазона чисел"""
#     attempt = 0
#     MAX_ATTEMPT = 100000
#     while True:
#         pic_name = str(random.randint(0, 100000))
#         filename_to_save = f"{pic_name}.{file_type}"
#         os_path = os.path.join(folder, filename_to_save)
#         is_filename_occupied = os.path.exists(os_path)
#
#         if not is_filename_occupied:
#             return filename_to_save
#         attempt += 1
#
#         if attempt > MAX_ATTEMPT:
#             raise OutOffFreeNamesError("No free Names to save Images")

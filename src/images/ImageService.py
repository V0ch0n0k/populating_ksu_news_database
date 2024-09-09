import os

from config import get_settings
from src.images.models import DType, Image, PictureType

__all__ = ["ImageService"]


class ImageService:

    def __init__(self, session, base_image_path: str | None = None):
        if base_image_path is None:
            base_image_path = f"{get_settings().BASE_RESOURCE_PATH}/images"

        self.session = session
        self.base_image_path = base_image_path

    def create_image(
        self, dtype: str, logo_type: int | None = None, file_name: str | None = None, file_path: str | None = None
    ) -> Image:
        if dtype not in DType.values():
            raise ValueError(f"dtype must be one of {DType.values()}")
        if dtype != DType.LOGO.value and logo_type is not None:
            raise ValueError("logo_type must be None if dtype is not DType.LOGO.value")

        if file_path is not None:
            full_file_path = file_path
        elif file_name is not None:
            full_file_path = os.path.join(self.base_image_path, os.path.basename(file_name))
        else:
            raise ValueError("Either file_name or file_path must be provided")

        picture_type_index = PictureType.get_picture_type_for_path(full_file_path).index
        with open(full_file_path, "rb") as file:
            image_data = file.read()

        image = Image(
            as_bytes=image_data,
            picture_type=picture_type_index,
            is_compressed=False,
            logo_type=logo_type,
            dtype=dtype,
        )
        self.session.add(image)
        return image

from enum import Enum as PyEnum
from pathlib import Path

from sqlalchemy import Boolean, Integer, LargeBinary, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.general.models import BaseModel

__all__ = ["PictureType", "Image", "DType"]


class PictureType(PyEnum):
    JPEG = "image/jpeg"
    PNG = "image/png"
    GIF = "image/gif"
    BMP = "image/bmp"
    SVG = "image/svg+xml"
    WEBP = "image/webp"

    @property
    def index(self):
        return list(PictureType).index(self)

    @staticmethod
    def get_picture_type_for_path(file_path: str) -> "PictureType":
        extension = Path(file_path).suffix.lower()
        mapping = {
            ".jpg": PictureType.JPEG,
            ".jpeg": PictureType.JPEG,
            ".png": PictureType.PNG,
            ".gif": PictureType.GIF,
            ".bmp": PictureType.BMP,
            ".svg": PictureType.SVG,
            ".webp": PictureType.WEBP,
        }
        return mapping.get(extension, PictureType.JPEG)


class DType(PyEnum):
    LOGO = "logo"
    IMAGES = "images"

    @property
    def index(self):
        return list(DType).index(self)

    @staticmethod
    def values():
        return [item.value for item in DType]


class Image(BaseModel):
    __tablename__ = "images"
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    as_bytes: Mapped[LargeBinary] = mapped_column(LargeBinary, nullable=False)
    is_compressed: Mapped[Boolean] = mapped_column(Boolean, nullable=False, default=False)
    picture_type: Mapped[SmallInteger] = mapped_column(SmallInteger, nullable=False)
    logo_type: Mapped[Integer] = mapped_column(Integer, nullable=True)
    dtype: Mapped[String] = mapped_column(String, nullable=False)

    def __str__(self):
        return f"<{self.__class__.__name__}(id={self.id}, picture_type={self.picture_type})>"

    def __repr__(self):
        return self.__str__()

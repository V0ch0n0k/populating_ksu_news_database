from sqlalchemy import BigInteger, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.general.models import BaseModel

__all__ = ["PartnerLocalization"]


class PartnerLocalization(BaseModel):
    __tablename__ = "partners_localizations"

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True)
    language: Mapped[SmallInteger] = mapped_column(SmallInteger, nullable=False)
    name: Mapped[String] = mapped_column(String, nullable=False)

    localization_mapping = relationship("PartnerLocalizationMapping", back_populates="localization")

    def __str__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name={self.name}), language={self.language}>"

    def __repr__(self):
        return self.__str__()

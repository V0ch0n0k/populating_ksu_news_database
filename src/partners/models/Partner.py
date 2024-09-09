from sqlalchemy import BigInteger, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.general.models import BaseModel

__all__ = ["Partner"]


class Partner(BaseModel):
    __tablename__ = "partners"

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True)
    source_language: Mapped[SmallInteger] = mapped_column(SmallInteger, nullable=False)
    url: Mapped[String] = mapped_column(String, nullable=False)
    country: Mapped[String] = mapped_column(String, nullable=False)
    partner_logo_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("images.id"), nullable=False)

    logo = relationship("Image")
    localization_mapping = relationship("PartnerLocalizationMapping", back_populates="partner")
    team_members = relationship("TeamMember", back_populates="partner")

    def __str__(self):
        return f"<{self.__class__.__name__}(id={self.id}, source_language={self.source_language})>"

    def __repr__(self):
        return self.__str__()

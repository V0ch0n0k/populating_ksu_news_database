from sqlalchemy import Boolean, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.general.models import BaseModel

__all__ = ["TeamMember"]


class TeamMember(BaseModel):
    __tablename__ = "team_members"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    source_language: Mapped[SmallInteger] = mapped_column(SmallInteger, nullable=False)
    team_photo_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("images.id"), nullable=True)
    gender: Mapped[Boolean] = mapped_column(Boolean, nullable=False, default=True)
    email: Mapped[String] = mapped_column(String, nullable=False)
    is_main: Mapped[Boolean] = mapped_column(Boolean, nullable=False)
    partner_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("partners.id"), nullable=False)

    photo = relationship("Image")
    partner = relationship("Partner", back_populates="team_members")
    localization_mapping = relationship("TeamMemberLocalizationMapping", back_populates="team_member")

    def __str__(self):
        return (
            f"<{self.__class__.__name__}(id={self.id}, source_language={self.source_language}, "
            f"partner_id={self.partner_id})>"
        )

    def __repr__(self):
        return self.__str__()

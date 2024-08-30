from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel


class Team(BaseModel):
    __tablename__ = 'team'
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    name: Mapped[String] = mapped_column(String, nullable=False)
    title: Mapped[String] = mapped_column(String, nullable=False)
    experience: Mapped[String] = mapped_column(String, nullable=False)
    caption: Mapped[String] = mapped_column(String, nullable=False)
    team_photo_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('images.id'), nullable=False)
    photo = relationship('Image')
    gender: Mapped[Boolean] = mapped_column(Boolean, nullable=False)
    is_main: Mapped[Boolean] = mapped_column(Boolean, nullable=False)
    partner_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('partners.id'), nullable=False)
    partner = relationship("Partner", back_populates="team_members")

    def __str__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name={self.name})>"

    def __repr__(self):
        return self.__str__()

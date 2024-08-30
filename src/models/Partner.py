from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel


class Partner(BaseModel):
    __tablename__ = 'partners'
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    name: Mapped[String] = mapped_column(String, nullable=False)
    url: Mapped[String] = mapped_column(String, nullable=False)
    email: Mapped[String] = mapped_column(String, nullable=False)
    partner_logo_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('images.id'), nullable=False)
    logo = relationship('Image')
    team_members = relationship("Team", back_populates="partner", cascade="all, delete-orphan")

    def __str__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name={self.name})>"

    def __repr__(self):
        return self.__str__()

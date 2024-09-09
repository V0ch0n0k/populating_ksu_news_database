from sqlalchemy import Integer, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.general.models import BaseModel

__all__ = ["TeamMemberLocalization"]


class TeamMemberLocalization(BaseModel):
    __tablename__ = "team_members_localizations"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    language: Mapped[SmallInteger] = mapped_column(SmallInteger, nullable=False)
    name: Mapped[String] = mapped_column(String, nullable=False)
    title: Mapped[Text] = mapped_column(Text, nullable=False)
    experience: Mapped[Text] = mapped_column(Text, nullable=False)
    caption: Mapped[Text] = mapped_column(Text, nullable=False)
    degree: Mapped[String] = mapped_column(String, nullable=True)
    institution: Mapped[String] = mapped_column(String, nullable=True)

    localization_mapping = relationship("TeamMemberLocalizationMapping", back_populates="localization")

    def __str__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name={self.name}), language={self.language}>"

    def __repr__(self):
        return self.__str__()

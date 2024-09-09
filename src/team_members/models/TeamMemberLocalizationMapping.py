from sqlalchemy import BigInteger, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.general.models import BaseModel

__all__ = ["TeamMemberLocalizationMapping"]


class TeamMemberLocalizationMapping(BaseModel):
    __tablename__ = "team_member_localization_mapping"

    team_members_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey("team_members.id"), primary_key=True)
    localizations_id: Mapped[BigInteger] = mapped_column(
        BigInteger, ForeignKey("team_members_localizations.id"), unique=True
    )
    localizations_key: Mapped[SmallInteger] = mapped_column(SmallInteger, nullable=False, primary_key=True)

    team_member = relationship("TeamMember", back_populates="localization_mapping")
    localization = relationship("TeamMemberLocalization", back_populates="localization_mapping")

    def __str__(self):
        return (
            f"<{self.__class__.__name__}(team_members_id={self.team_members_id}, "
            f"localizations_id={self.localizations_id}, localizations_key={self.localizations_key})>"
        )

    def __repr__(self):
        return self.__str__()

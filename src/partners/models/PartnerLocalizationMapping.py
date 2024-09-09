from sqlalchemy import BigInteger, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.general.models import BaseModel

__all__ = ["PartnerLocalizationMapping"]


class PartnerLocalizationMapping(BaseModel):
    __tablename__ = "partner_localization_mapping"

    partners_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey("partners.id"), primary_key=True)
    localizations_id: Mapped[BigInteger] = mapped_column(
        BigInteger, ForeignKey("partners_localizations.id"), unique=True
    )
    localizations_key: Mapped[SmallInteger] = mapped_column(SmallInteger, nullable=False, primary_key=True)

    partner = relationship("Partner", back_populates="localization_mapping")
    localization = relationship("PartnerLocalization", back_populates="localization_mapping")

    def __str__(self):
        return (
            f"<{self.__class__.__name__}(partners_id={self.partners_id}, localizations_id={self.localizations_id}, "
            f" localizations_key={self.localizations_key})>"
        )

    def __repr__(self):
        return self.__str__()

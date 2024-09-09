from typing import Dict, List

from src.images import ImageService
from src.images.models import DType
from src.partners.models import Partner, PartnerLocalization, PartnerLocalizationMapping

__all__ = ["PartnerService"]


class PartnerService:
    def __init__(self, session):
        self.session = session
        self.image_service = ImageService(session)

    def create_partner(self, source_language: int, data: Dict) -> Partner:
        partner = Partner(
            source_language=source_language,
            url=data["url"],
            country=data["country"],
            logo=self.image_service.create_image(
                file_path=data["logo_path"],
                logo_type=data["logo_type"],
                dtype=DType.LOGO.value,
            ),
        )
        self.session.add(partner)
        return partner

    def add_localization(self, partner_id: int, localization: Dict) -> PartnerLocalization:
        partnerLocalization = PartnerLocalization(
            language=localization["language"],
            name=localization["name"],
        )

        self.session.add(partnerLocalization)
        self.session.flush()

        mapping = PartnerLocalizationMapping(
            partners_id=partner_id,
            localizations_id=partnerLocalization.id,
            localizations_key=partnerLocalization.language,
        )

        self.session.add(mapping)
        return partnerLocalization

    def add_localizations(self, partner_id: int, localizations: List[Dict]) -> List[PartnerLocalization]:
        partnerLocalization_list = [
            PartnerLocalization(
                language=loc["language"],
                name=loc["name"],
            )
            for loc in localizations
        ]
        self.session.add_all(partnerLocalization_list)
        self.session.flush()

        mapping_list = [
            PartnerLocalizationMapping(
                partners_id=partner_id,
                localizations_id=partnerLocalization.id,
                localizations_key=partnerLocalization.language,
            )
            for partnerLocalization in partnerLocalization_list
        ]
        self.session.add_all(mapping_list)
        return partnerLocalization_list

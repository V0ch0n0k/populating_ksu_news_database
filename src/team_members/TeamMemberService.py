from typing import Dict, List

from src.images import ImageService
from src.images.models import DType
from src.team_members.models import TeamMember, TeamMemberLocalization, TeamMemberLocalizationMapping

from .TeamMemberUtil import TeamMemberUtil

__all__ = ["TeamMemberService"]


class TeamMemberService:
    def __init__(self, session):
        self.session = session
        self.image_service = ImageService(session)

    def create_team_member(self, source_language: int, partner_id: int, data: Dict) -> TeamMember:
        team_member = TeamMember(
            partner_id=partner_id,
            source_language=source_language,
            photo=(
                self.image_service.create_image(
                    file_path=data["photo_path"],
                    dtype=DType.IMAGES.value,
                )
                if data.get("photo_path")
                else None
            ),
            gender=TeamMemberUtil.is_male(data["gender"], default=True),
            email=data["email"],
            is_main=data["is_main"],
        )
        self.session.add(team_member)
        return team_member

    def add_localization(self, team_member_id: int, localization: Dict) -> TeamMemberLocalization:
        print(f"localization={localization}")
        teamMemberLocalization = TeamMemberLocalization(
            name=localization["name"],
            language=localization["language"],
            title=localization["title"],
            experience=localization["experience"],
            caption=localization["caption"],
            degree=localization.get("degree"),
            institution=localization.get("institution"),
        )

        self.session.add(teamMemberLocalization)
        self.session.flush()

        mapping = TeamMemberLocalizationMapping(
            team_members_id=team_member_id,
            localizations_id=teamMemberLocalization.id,
            localizations_key=teamMemberLocalization.language,
        )

        self.session.add(mapping)
        return teamMemberLocalization

    def add_localizations(self, team_member_id: int, localizations: List[Dict]) -> List[TeamMemberLocalization]:

        teamMemberLocalization_list = [
            TeamMemberLocalization(
                name=loc["name"],
                language=loc["language"],
                title=loc["title"],
                experience=loc["experience"],
                caption=loc["caption"],
                degree=loc.get("degree"),
                institution=loc.get("institution"),
            )
            for loc in localizations
        ]

        self.session.add_all(teamMemberLocalization_list)
        self.session.flush()

        mapping_list = [
            TeamMemberLocalizationMapping(
                team_members_id=team_member_id,
                localizations_id=teamMemberLocalization.id,
                localizations_key=teamMemberLocalization.language,
            )
            for teamMemberLocalization in teamMemberLocalization_list
        ]

        self.session.add_all(mapping_list)
        return teamMemberLocalization_list

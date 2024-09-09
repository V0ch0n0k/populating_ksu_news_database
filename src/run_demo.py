import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import get_settings
from general.util import load_data_from_json_by_path
from src.general.enums import Language
from src.general.models import BaseModel
from src.partners import PartnerService
from src.team_members import TeamMemberService

SOURCE_LANGUAGE_INDEX = Language.EN.index

IMAGE_PATH = f"{get_settings().BASE_RESOURCE_PATH}/demo_data"


def main():
    data = load_data_from_json_by_path(f"{get_settings().BASE_RESOURCE_PATH}/demo_data/data.json")

    partner_service = PartnerService(session)
    team_member_service = TeamMemberService(session)

    data["partner"]["logo_path"] = os.path.join(IMAGE_PATH, os.path.basename(data["partner"]["logo_path"]))
    partner = partner_service.create_partner(source_language=SOURCE_LANGUAGE_INDEX, data=data["partner"])
    session.flush()

    partner_localizations = [loc for loc in data["partner"]["localizations"]]
    partner_service.add_localizations(partner.id, partner_localizations)

    for member in data["team_member"]:
        member["photo_path"] = os.path.join(IMAGE_PATH, os.path.basename(member["photo_path"]))
        team_member = team_member_service.create_team_member(
            source_language=SOURCE_LANGUAGE_INDEX, partner_id=partner.id, data=member
        )
        session.flush()

        team_member_localizations = [loc for loc in member["localizations"]]
        team_member_service.add_localizations(team_member.id, team_member_localizations)

    session.commit()


if __name__ == "__main__":
    engine = create_engine(get_settings().get_db_url())
    engine.echo = True
    BaseModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    main()

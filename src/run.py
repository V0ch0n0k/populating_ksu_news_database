import json
import os
import re

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from config import get_settings
from general.enums import Language
from general.models import BaseModel
from partners import PartnerService
from team_members import TeamMemberService

SELECT_BY_PARTNER_FILE = True
DATA_JSON_PATH = f"{get_settings().BASE_RESOURCE_PATH}/data/"
PARTNER_IMAGE_PATH = f"{get_settings().BASE_RESOURCE_PATH}/data/images/partners/"
TEAM_MEMBER_IMAGE_PATH = f"{get_settings().BASE_RESOURCE_PATH}/data/images/partners/people/"
SOURCE_LANGUAGE_INDEX = Language.EN.index
MISSING_INFO = {
    Language.UK.index: "Інформація з'явиться найближчим часом.",
    Language.EN.index: "Information will appear soon.",
}


def remove_last_colon(text: str) -> str:
    return re.sub(r":\s*$", "", text)


def load_data():
    with (
        open(f"{DATA_JSON_PATH}team.json", "r", encoding="utf-8") as team_file,
        open(f"{DATA_JSON_PATH}partners.json", "r", encoding="utf-8") as partners_file,
        open(f"{DATA_JSON_PATH}uk.json", "r", encoding="utf-8") as uk_localization_file,
        open(f"{DATA_JSON_PATH}en.json", "r", encoding="utf-8") as en_localization_file,
    ):
        team_data = json.load(team_file)
        partners_data = json.load(partners_file)
        uk_localization_data = json.load(uk_localization_file)
        en_localization_data = json.load(en_localization_file)
    return team_data, partners_data, uk_localization_data, en_localization_data


def process_team_data(team_data):
    team_member_dict = {}
    for role, role_group in team_data.items():
        for member in role_group:
            team_member_dict[member["key"]] = {
                "gender": member.get("gender", None),
                "photo": member.get("photo", None),
            }
    return team_member_dict


def process_partner_localizations(partner_service, partner_id, partner_translationKey, localization_data_dict):
    list_of_localizations = []
    for language_index, localization_data in localization_data_dict.items():
        paertner_localization_data = localization_data["partners"][partner_translationKey]
        list_of_localizations.append(
            {
                "language": language_index,
                "name": paertner_localization_data["title"],
            },
        )
    partnerLocalization_list = partner_service.add_localizations(partner_id, list_of_localizations)
    # print(f"partnerLocalization_list: {partnerLocalization_list}")


def process_team_localizations(
    team_member_service,
    partner_id,
    members_keys,
    target_members_initial_data_dict,
    partner_info,
    localization_data_dict,
):
    team_datas = {}
    for language_index, localization_data in localization_data_dict.items():
        for member_translation_key in members_keys:

            member_initial_data = target_members_initial_data_dict.get(member_translation_key, {})

            member_in_partner = localization_data["partners"][partner_info["translationKey"]]["people"][
                member_translation_key
            ]

            team_localization_data = localization_data["about"]["team"]
            if team_localization_data["coordinators"]["list"].get(member_translation_key) is not None:
                member_localization_data = team_localization_data["coordinators"]["list"][member_translation_key]

                name, degree = member_localization_data.get("name", None), member_localization_data.get("degree", None)
                if name is not None:
                    lst = [part.strip() for part in name.split(",", 1)]
                    if len(lst) == 2:
                        name, degree = lst
                member_localization_data = {
                    "name": name,
                    "degree": degree,
                    "role": member_localization_data.get("role", "coordinators"),
                    "title": member_localization_data.get("role", remove_last_colon(member_in_partner["role"])),
                    "experience": member_localization_data.get("experience", None),
                    "caption": member_localization_data.get("description", None),
                    "institution": member_localization_data.get("institution", None),
                    "photo": member_localization_data.get("photo", None),
                }

            elif team_localization_data["list"].get(member_translation_key) is not None:
                regular_members = team_localization_data["list"]

                member_localization_data = regular_members[member_translation_key]
                name, degree = member_localization_data.get("name", None), member_localization_data.get("degree", None)
                if name is not None:
                    lst = [part.strip() for part in name.split(",", 1)]
                    if len(lst) == 2:
                        name, degree = lst
                member_localization_data = {
                    "name": name,
                    "degree": degree,
                    "role": member_localization_data.get("role", "all"),
                    "title": member_localization_data.get("role", remove_last_colon(member_in_partner["role"])),
                    "experience": member_localization_data.get("experience", None),
                    "caption": member_localization_data.get("position", None),
                    "institution": member_localization_data.get("institution", None),
                    "photo": member_localization_data.get("photo", None),
                }
            else:
                member_localization_data = member_in_partner

                name, degree = member_localization_data.get("name", None), member_localization_data.get("degree", None)
                if name is not None:
                    lst = [part.strip() for part in name.split(",", 1)]
                    if len(lst) == 2:
                        name, degree = lst
                member_localization_data = {
                    "name": member_localization_data["name"],
                    "degree": degree,
                    "role": member_localization_data.get("role", "all"),
                    "title": member_localization_data.get("role", remove_last_colon(member_in_partner["role"])),
                    "experience": member_localization_data.get("experience", None),
                    "caption": member_localization_data.get("position", None),
                    "institution": member_localization_data.get("institution", None),
                    "photo": member_localization_data.get("photo", None),
                }

            if member_translation_key not in team_datas:
                team_datas[member_translation_key] = {}
                team_datas[member_translation_key]["localizations"] = {}

            if team_datas[member_translation_key].get("basic") is None:

                team_datas[member_translation_key]["basic"] = {
                    "email": member_initial_data.get("email", None),
                    "gender": member_initial_data.get("gender", None),
                    "is_main": member_localization_data["role"] == "coordinators",
                }

            if team_datas[member_translation_key]["basic"].get("photo_path") is None:
                member_photo = member_initial_data.get("photo", member_localization_data.get("photo", None))

                team_datas[member_translation_key]["basic"]["photo_path"] = (
                    os.path.join(TEAM_MEMBER_IMAGE_PATH, os.path.basename(member_photo))
                    if member_photo is not None
                    else None
                )

            team_datas[member_translation_key]["localizations"][language_index] = {
                "language": language_index,
                "name": member_localization_data["name"],
                "title": (
                    member_localization_data.get("title")
                    if member_localization_data.get("title")
                    else MISSING_INFO[language_index]
                ),
                "experience": (
                    member_localization_data.get("experience")
                    if member_localization_data.get("experience")
                    else MISSING_INFO[language_index]
                ),
                "caption": (
                    member_localization_data.get("caption")
                    if member_localization_data.get("caption")
                    else MISSING_INFO[language_index]
                ),
                "degree": (
                    member_localization_data.get("degree")
                    if member_localization_data.get("degree")
                    else MISSING_INFO[language_index]
                ),
                "institution": (
                    member_localization_data.get("institution")
                    if member_localization_data.get("institution")
                    else MISSING_INFO[language_index]
                ),
            }

    for member_translation_key, datas in team_datas.items():
        team_member = team_member_service.create_team_member(
            source_language=SOURCE_LANGUAGE_INDEX, partner_id=partner_id, data=datas["basic"]
        )
        session.flush()
        teamMemberLocalization_list = team_member_service.add_localizations(
            team_member_id=team_member.id,
            localizations=[localization for localization in datas["localizations"].values()],
        )

        # print(f"teamMemberLocalization_list: {teamMemberLocalization_list}")


def main():
    ## Restart sequence
    # session.execute(text("ALTER SEQUENCE images_id_seq RESTART WITH 93;"))
    # session.commit()

    team_data, partners_data, uk_localization_data, en_localization_data = load_data()
    target_members_initial_data_dict = process_team_data(team_data)
    localization_data_dict = {
        Language.EN.index: en_localization_data,
        Language.UK.index: uk_localization_data,
    }

    partner_service = PartnerService(session)
    team_member_service = TeamMemberService(session)

    for partner_info in partners_data:
        members_keys = []
        for partner_member_info in partner_info["people"]:
            if (
                not SELECT_BY_PARTNER_FILE
                and partner_member_info["translationKey"] not in target_members_initial_data_dict.keys()
            ):
                print(f"Skipping {partner_member_info['translationKey']}")
                continue

            members_keys.append(partner_member_info["translationKey"])

            if target_members_initial_data_dict.get(partner_member_info["translationKey"]) is None:
                target_members_initial_data_dict[partner_member_info["translationKey"]] = {}

            target_members_initial_data_dict[partner_member_info["translationKey"]]["email"] = partner_member_info[
                "email"
            ]

        if len(members_keys) == 0:
            continue

        partner_data = {
            "url": partner_info["link"],
            "country": partner_info["country"],
            "logo_path": (
                os.path.join(PARTNER_IMAGE_PATH, os.path.basename(partner_info["logo"]))
                if partner_info.get("logo")
                else None
            ),
            "logo_type": partner_info.get("logoType", None),
        }

        partner = partner_service.create_partner(source_language=SOURCE_LANGUAGE_INDEX, data=partner_data)
        session.flush()

        # Add partner localizations
        process_partner_localizations(
            partner_service,
            partner.id,
            partner_info["translationKey"],
            localization_data_dict,
        )

        # Add team member localizations for the partner
        process_team_localizations(
            team_member_service,
            partner.id,
            members_keys,
            target_members_initial_data_dict,
            partner_info,
            localization_data_dict,
        )

        session.commit()


if __name__ == "__main__":
    engine = create_engine(get_settings().get_db_url())
    engine.echo = True
    BaseModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    main()

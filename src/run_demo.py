import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import BaseModel, Image, Partner, PictureType, Team

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
engine.echo = True
BaseModel.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def create_image(file_path: str) -> Image:
    picture_type_index = PictureType.get_picture_type_for_path(file_path).index
    with open(file_path, "rb") as file:
        image_data = file.read()
    return Image(as_bytes=image_data, picture_type=picture_type_index, is_compressed=False)


def main():
    partner = Partner(
        name='Example Partner',
        url='https://example.com',
        email='contact@example.com',
        logo=create_image('../images/partner_logo.svg')
    )

    list_partners = [
        Team(
            name='John Doe',
            title='Software Engineer',
            experience='5 years',
            caption='Expert in backend development',
            photo=create_image('../images/team_photo_1.png'),
            gender=True,
            is_main=True,
            partner=partner
        ),
        Team(
            name='Jane Smith',
            title='Product Manager',
            experience='7 years',
            caption='Specialist in product lifecycle management',
            photo=create_image('../images/team_photo_2.jpg'),
            gender=False,
            is_main=False,
            partner=partner
        )]

    partner.team_members = list_partners

    session.add(partner)
    session.commit()


if __name__ == '__main__':
    main()

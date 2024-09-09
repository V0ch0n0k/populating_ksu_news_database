from enum import Enum as PyEnum


class Language(PyEnum):
    EN = "en"
    UK = "uk"

    @property
    def index(self):
        return list(Language).index(self)

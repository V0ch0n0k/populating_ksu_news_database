__all__ = ["TeamMemberUtil"]


class TeamMemberUtil:

    @staticmethod
    def is_male(gender_str: str | None, default: bool) -> bool:
        if gender_str is None:
            if default is None:
                raise ValueError("Default value must be boolean")
            return default

        if not isinstance(gender_str, str):
            raise ValueError("Value must be a string")

        match gender_str.upper():
            case "M":
                return True
            case "F":
                return False
            case _:
                raise ValueError("Gender must be 'M' or 'F'")

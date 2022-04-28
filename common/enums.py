from enum import Enum


class UserTypes(Enum):
    CustomUser = "User"
    AdminUser = "Admin"

    @staticmethod
    def get_enums():
        return [
            (enum_cutomuser_type.name, enum_cutomuser_type.value)
            for enum_cutomuser_type in UserTypes
        ]

from enum import Enum


class AccountRoleID(Enum):
    BROKER_PUBLISHER = 1
    BROKER_SUBSCRIBER = 2
    BROKER_VIEWER = 3
    STORAGE_WRITER = 4
    STORAGE_READER = 5

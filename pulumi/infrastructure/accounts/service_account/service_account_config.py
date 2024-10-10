from infrastructure.accounts.AccountRoleID import AccountRoleID

ROLE_DEFINITIONS = {
    AccountRoleID.BROKER_PUBLISHER: {
        "name": "publisher",
        "id": "roles/pubsub.publisher",
    },
    AccountRoleID.BROKER_SUBSCRIBER: {
        "name": "subscriber",
        "id": "roles/pubsub.subscriber",
    },
    AccountRoleID.BROKER_VIEWER: {
        "name": "viewer",
        "id": "roles/pubsub.viewer",
    },
    AccountRoleID.STORAGE_WRITER: {
        "name": "legacyBucketWriter",
        "id": "roles/storage.legacyBucketWriter",
    },
    AccountRoleID.STORAGE_READER: {
        "name": "objectViewer",
        "id": "roles/storage.objectViewer",
    },
}

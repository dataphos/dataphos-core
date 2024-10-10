from infrastructure.accounts.AccountRoleID import AccountRoleID

ROLE_DEFINITIONS = {
    AccountRoleID.BROKER_PUBLISHER: {
        "name": "Azure Service Bus Data Sender",
        "id": "69a216fc-b8fb-44d8-bc22-1f3c2cd27a39",
    },
    AccountRoleID.BROKER_SUBSCRIBER: {
        "name": "Azure Service Bus Data Receiver",
        "id": "4f6d3b9b-027b-4f4c-9142-0e5a2a2247e0",
    },
    AccountRoleID.STORAGE_WRITER: {
        "name": "Storage Blob Data Contributor",
        "id": "ba92f5b4-2d11-453d-a403-e96b0029c9fe",
    },
    AccountRoleID.STORAGE_READER: {
        "name": "Storage Blob Data Reader",
        "id": "2a2b9908-6ea1-4ae2-8e65-a410df84e7d1",
    },
}

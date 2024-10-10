# Copyright 2024 Syntio Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

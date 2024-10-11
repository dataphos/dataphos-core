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

from abc import ABC, abstractmethod

from infrastructure.ResourceCreator import ResourceCreator


class AbstractMessageBroker(ABC, ResourceCreator):

    @abstractmethod
    def add_topic(self, topic_name: str, topic_config: dict):
        raise NotImplementedError

    @abstractmethod
    def add_subscription(self, topic_name: str, subscription_name: str, subscription_config: dict):
        raise NotImplementedError

    @abstractmethod
    def export_config(self) -> dict:
        raise NotImplementedError

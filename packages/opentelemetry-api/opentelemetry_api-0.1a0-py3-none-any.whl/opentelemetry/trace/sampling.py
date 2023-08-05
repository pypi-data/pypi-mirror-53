# Copyright 2019, OpenTelemetry Authors
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

from typing import Dict, Optional
from opentelemetry.trace import SpanContext
from opentelemetry.types import AttributeValue
import abc


class Decision:
    """Don't forget to move this up to the class docstring!

    Args:
        sampled: (description)
        attributes: (description)
    """

    def __init__(self,
                 sampled: bool = False,
                 attributes: Dict[str, "AttributeValue"] = None
                 ) -> None:
        self.sampled = sampled
        if attributes is None:
            self.attributes = {}
        self.attributes = attributes


class Sampler(abc.ABC):
    """Docstring for Sampler. """

    @abc.abstractmethod
    def should_sample(
            self,
            parent_context: Optional["SpanContext"],
            remote: Optional[bool],
            trace_id: int,
            span_id: int,
            name: str,
    ) -> "Decision":
        """Docstring for should_sample. """


class AlwaysSampleSampler(Sampler):
    def should_sample(
            self,
            parent_context: Optional["SpanContext"],
            remote: Optional[bool],
            trace_id: int,
            span_id: int,
            name: str,
    ) -> bool:
        return Decision(True)


class NeverSampleSampler(Sampler):
    def should_sample(
            self,
            parent_context: Optional["SpanContext"],
            remote: Optional[bool],
            trace_id: int,
            span_id: int,
            name: str,
    ) -> bool:
        return Decision(False)

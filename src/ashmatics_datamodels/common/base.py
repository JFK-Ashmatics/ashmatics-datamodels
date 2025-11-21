# Copyright 2025 Asher Informatics PBC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Base model classes for all AshMatics schemas.

These models are database-agnostic and provide common configuration
and functionality across all domain-specific schemas.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AshMaticsBaseModel(BaseModel):
    """
    Base model for all AshMatics schemas.

    Configuration:
        - from_attributes: Enable ORM mode for SQLAlchemy integration in apps
        - validate_assignment: Validate on field assignment
        - use_enum_values: Use enum values, not names, in serialization
        - extra: Forbid extra fields by default for strict validation
        - str_strip_whitespace: Strip whitespace from string fields
    """

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        extra="forbid",
        str_strip_whitespace=True,
    )


class TimestampedModel(AshMaticsBaseModel):
    """
    Model with creation and update timestamps.

    Use for entities that need temporal tracking but not full audit trails.
    """

    created_at: Optional[datetime] = Field(
        None, description="Timestamp when record was created"
    )
    updated_at: Optional[datetime] = Field(
        None, description="Timestamp when record was last updated"
    )


class AuditedModel(TimestampedModel):
    """
    Model with full audit trail support.

    Use for entities requiring user attribution for changes.
    """

    created_by: Optional[str] = Field(
        None, description="User ID or system identifier who created the record"
    )
    updated_by: Optional[str] = Field(
        None, description="User ID or system identifier who last updated the record"
    )

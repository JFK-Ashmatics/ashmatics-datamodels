# Copyright 2026 Asher Informatics PBC
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
ActionAuthority's home and its compatibility re-export (0.15.0).

It moved from ``failure_modes`` to ``common`` because it classifies the
SYSTEM, not the thing conditioning on it, and two modules now condition on
it. The re-export is what keeps that move non-breaking.

This exists because the re-export is load-bearing but reads as an unused
import: ``ruff --fix`` deleted it once during the move, which would have
broken every existing ``from ashmatics_datamodels.failure_modes import
ActionAuthority`` silently. A ``# noqa`` comment is the fix; this is the
guard, because comments can be removed and tests argue back.
"""

from ashmatics_datamodels.common import ActionAuthority as FromCommonPackage
from ashmatics_datamodels.common.enums import ActionAuthority as FromCommon
from ashmatics_datamodels.failure_modes import ActionAuthority as FromFMPackage
from ashmatics_datamodels.failure_modes.enums import ActionAuthority as FromFM


def test_every_import_path_yields_the_same_enum():
    assert FromCommon is FromCommonPackage is FromFM is FromFMPackage


def test_canonical_home_is_common():
    assert FromCommon.__module__ == "ashmatics_datamodels.common.enums"


def test_values_are_concept_local_names():
    """
    ash facet convention, shared by the method and failure-mode
    applicability axes. Notations differ from local names for the ash facet
    concepts, so this is the half that must not drift.
    """
    assert {m.value for m in FromCommon} == {
        "aa-recommend-only",
        "aa-act-with-approval",
        "aa-act-autonomously",
    }

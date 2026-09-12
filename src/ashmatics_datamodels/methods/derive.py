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
Derivations over an approved method set (ADR-022 D6, ASHFORGE-370).

D6 requires provenance **per member**: which methods in an approved set carry
Asher's warrant as exemplars, and which the organization adjudicated in for
itself. ``delivery_mode`` is set-level and cannot answer it.

**Derived, not stored**, for the reason ADR-022 D6 states in its own text: the
adjudicated origin is "already expressible today as a ``MethodSetAdjustment``
with its mandatory ``rationale``", and the exemplar origin is membership in the
set's inherited ``members`` baseline. Both facts are already written. What was
missing is the per-member *view* of them, which is a join, not a field.

Storing it instead would give "where did this method come from" two answers
that can disagree — the same defect ``registry.derive.system_class`` exists to
avoid (see that module, and the 0.12.0 changelog entry: "adding a second stored
field for the same fact would give two answers that can disagree"). It also
keeps ``resolved_members`` unchanged, so nothing downstream re-pins.

Invalid or unattributable input raises ``ValueError`` rather than degrading,
the same fail-loudly posture as the registry derivations.
"""

from .enums import MemberProvenance, MethodPhase
from .method_sets import ApprovedMethodSet, MemberPhase, MethodId


def _adjudicated_ids(
    approved: ApprovedMethodSet, phase: MemberPhase
) -> set[MethodId]:
    """
    Method ids the org adjudicated INTO the set for this phase.

    Only ``added`` confers adjudicated provenance. ``reranked`` changes order
    and leaves a member whatever it already was; ``removed`` members are not
    in ``resolved_members`` at all.

    ``MethodPhase.BOTH`` on an adjustment covers both concrete phases, since
    ``resolved_members`` is only ever keyed by the two.
    """
    return {
        adj.method_id
        for adj in approved.adjustments
        if adj.action == "added"
        and adj.phase in (phase, MethodPhase.BOTH, MethodPhase.BOTH.value)
    }


def member_provenance(
    approved: ApprovedMethodSet,
) -> dict[MemberPhase, dict[MethodId, MemberProvenance]]:
    """
    Origin of every resolved member, keyed by phase then method id.

    A member is ``ASHER_EXEMPLAR`` when it is in the exemplar baseline
    (``members``) for that phase, and ``ORGANIZATIONALLY_ADJUDICATED`` when an
    ``added`` adjustment brought it in. The baseline wins if a member is
    somehow both: it already carried Asher's warrant, and an adjustment that
    re-adds it changes nothing about where it came from.

    Raises ``ValueError`` for a member that is in neither, which is
    inconsistent data rather than a third kind of origin — so this doubles as
    a consistency check on the set. **Callers rendering an artifact should
    expect that**, and it is deliberate: returning a silent default would make
    an unattributable member indistinguishable from a warranted one, which is
    the confusion D6 exists to prevent.
    """
    out: dict[MemberPhase, dict[MethodId, MemberProvenance]] = {}
    for phase, resolved in approved.resolved_members.items():
        baseline = set(approved.members.get(phase) or [])
        adjudicated = _adjudicated_ids(approved, phase)
        per_phase: dict[MethodId, MemberProvenance] = {}
        for method_id in resolved:
            if method_id in baseline:
                per_phase[method_id] = MemberProvenance.ASHER_EXEMPLAR
            elif method_id in adjudicated:
                per_phase[method_id] = (
                    MemberProvenance.ORGANIZATIONALLY_ADJUDICATED
                )
            else:
                raise ValueError(
                    f"{approved.set_id}: resolved member {method_id!r} "
                    f"(phase {phase!r}) is in neither the exemplar baseline "
                    f"nor an 'added' adjustment, so its provenance cannot be "
                    f"established. Either it belongs in members, or the "
                    f"adjustment that introduced it is missing."
                )
        out[phase] = per_phase
    return out

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
Registry vocabulary freeze + derivation behavior (ASHFORGE-412).

The freeze tests assert the exact value sets, not just shapes: these are
rule-engine keys, and an "innocent rename" must fail here before it reaches a
migration (SRS-REG-AC-6). Deployment is asserted as an ordered tuple because
its order is part of the contract (SRS-REG-03).
"""

import pytest

from ashmatics_datamodels.registry import (
    DeploymentStatus,
    OrgSourcingMix,
    PortfolioSizeBucket,
    RegistryAIType,
    RegistryCategory,
    RegistryDeployment,
    RegistrySourcing,
    SourcingChannel,
    SystemClass,
    is_clinical_use,
    org_sourcing_mix,
    portfolio_size_bucket,
    sourcing_obligation,
    system_class,
)

# ── Vocabulary freeze ────────────────────────────────────────────────────────


def test_category_values_frozen():
    assert [m.value for m in RegistryCategory] == [
        "clinical",
        "operational",
        "administrative",
    ]


def test_aitype_values_frozen():
    assert [m.value for m in RegistryAIType] == [
        "predictive",
        "generative",
        "agentic",
        "other",
    ]


def test_sourcing_values_frozen():
    assert [m.value for m in SourcingChannel] == [
        "commercial",
        "ehr_embedded",
        "homegrown",
        "research",
    ]
    assert [m.value for m in RegistrySourcing] == ["vendor", "in_house", "hybrid"]


def test_deployment_values_frozen_in_order():
    # Order is meaningful: device → cloud, with the chosen-unknown sentinel last.
    # ehr/enterprise_system/agentic_platform added ASHFORGE-530/-534.
    assert [m.value for m in RegistryDeployment] == [
        "embedded",
        "pacs",
        "ehr",
        "enterprise_system",
        "platform",
        "agentic_platform",
        "onprem",
        "cloud",
        "unknown",
    ]


def test_deployment_status_values_frozen():
    # Order is the lifecycle, so position is a claim. `investigational` sits after
    # `validating` and before `live` because it is a stage a deployment can be in
    # before becoming standard of care — not because every investigational
    # deployment goes live; many do not. Added by ontology ADR-008 (seed v2.4.0):
    # an IRB-reviewed research deployment, distinguished from `pilot` by oversight
    # rather than scale.
    assert [m.value for m in DeploymentStatus] == [
        "evaluating",
        "pilot",
        "validating",
        "investigational",
        "live",
        "paused",
        "retired",
    ]


def test_derived_vocabularies_frozen():
    assert [m.value for m in PortfolioSizeBucket] == [
        "none",
        "small",
        "medium",
        "large",
        "extensive",
    ]
    assert [m.value for m in OrgSourcingMix] == [
        "vendor_only",
        "mostly_vendor",
        "mixed",
        "mostly_internal",
        "internal_only",
    ]
    # ADR-015 D4: class ids are kebab-case, unlike the snake_case used
    # everywhere else in this module. CHAR's validate_registry.py enforces the
    # same rule on the registry side; this freeze is the contract half.
    assert [m.value for m in SystemClass] == [
        "clinical",
        "administrative-operational",
    ]


# ── is_clinical_use (AC-2) ───────────────────────────────────────────────────


def test_is_clinical_use_truth_table():
    assert is_clinical_use(RegistryCategory.CLINICAL) is True
    assert is_clinical_use("clinical") is True
    assert is_clinical_use(RegistryCategory.OPERATIONAL) is False
    assert is_clinical_use("administrative") is False
    assert is_clinical_use(None) is False  # uncharacterized ⇒ no inferred obligation


def test_is_clinical_use_rejects_unknown_vocabulary():
    with pytest.raises(ValueError):
        is_clinical_use("clinical_use")  # the retired boolean's name, not a category


# ── system_class (ADR-015) ──────────────────────────────────────────────────────


def test_system_class_truth_table():
    assert system_class(RegistryCategory.CLINICAL) is SystemClass.CLINICAL
    assert system_class("clinical") is SystemClass.CLINICAL
    assert (
        system_class(RegistryCategory.OPERATIONAL)
        is SystemClass.ADMINISTRATIVE_OPERATIONAL
    )
    assert system_class("administrative") is SystemClass.ADMINISTRATIVE_OPERATIONAL


def test_system_class_uncharacterized_is_none_not_a_class():
    """ADR-015 D3.1: absent class means CHAR core content, not a class.

    Falling back to a class here would silently apply one class's
    specializations to a system nobody has classified — the reason this
    returns ``None`` rather than the majority value.
    """
    assert system_class(None) is None


def test_system_class_rejects_unknown_vocabulary():
    with pytest.raises(ValueError):
        # The CHAR-side class id is not a RegistryCategory value; passing one
        # back in is the round-trip mistake this guards.
        system_class("administrative-operational")


def test_system_class_and_is_clinical_use_agree_on_the_clinical_edge():
    """The two derivations read the same stored triad and must never disagree
    about which side of the clinical edge an entry falls on — that agreement is
    the whole reason neither is stored."""
    for category in RegistryCategory:
        assert is_clinical_use(category) == (
            system_class(category) is SystemClass.CLINICAL
        )


# ── portfolio_size_bucket (AC-3) ─────────────────────────────────────────────


@pytest.mark.parametrize(
    ("count", "expected"),
    [
        (0, PortfolioSizeBucket.NONE),
        (1, PortfolioSizeBucket.SMALL),
        (3, PortfolioSizeBucket.SMALL),
        (4, PortfolioSizeBucket.MEDIUM),
        (10, PortfolioSizeBucket.MEDIUM),
        (11, PortfolioSizeBucket.LARGE),
        (25, PortfolioSizeBucket.LARGE),
        (26, PortfolioSizeBucket.EXTENSIVE),
        (400, PortfolioSizeBucket.EXTENSIVE),
    ],
)
def test_portfolio_size_bucket_boundaries(count, expected):
    assert portfolio_size_bucket(count) is expected


def test_portfolio_size_bucket_rejects_negative():
    with pytest.raises(ValueError):
        portfolio_size_bucket(-1)


# ── sourcing_obligation (SRS-REG-15a, derived) ───────────────────────────────


@pytest.mark.parametrize(
    ("channel", "adapted", "expected"),
    [
        ("commercial", False, RegistrySourcing.VENDOR),
        ("ehr_embedded", False, RegistrySourcing.VENDOR),
        ("homegrown", False, RegistrySourcing.IN_HOUSE),
        ("research", False, RegistrySourcing.IN_HOUSE),
        # local adaptation is the only path to HYBRID, and only from a
        # vendor-obligation channel
        ("commercial", True, RegistrySourcing.HYBRID),
        ("ehr_embedded", True, RegistrySourcing.HYBRID),
        ("homegrown", True, RegistrySourcing.IN_HOUSE),
        ("research", True, RegistrySourcing.IN_HOUSE),
    ],
)
def test_sourcing_obligation(channel, adapted, expected):
    assert sourcing_obligation(channel, locally_adapted=adapted) is expected


def test_sourcing_obligation_uncharacterized_and_invalid():
    assert sourcing_obligation(None) is None
    with pytest.raises(ValueError):
        sourcing_obligation("vendor")  # an obligation value, not a channel


# ── org_sourcing_mix (AC-3) ──────────────────────────────────────────────────


def test_org_sourcing_mix_empty_and_uncharacterized_yield_none():
    assert org_sourcing_mix([]) is None
    assert org_sourcing_mix([None, None]) is None


@pytest.mark.parametrize(
    ("sourcings", "expected"),
    [
        (["vendor"] * 3, OrgSourcingMix.VENDOR_ONLY),
        (["in_house"] * 3, OrgSourcingMix.INTERNAL_ONLY),
        (["hybrid"] * 4, OrgSourcingMix.MIXED),  # all-hybrid reads as mixed
        (["vendor"] * 4 + ["in_house"], OrgSourcingMix.MOSTLY_VENDOR),  # 0.8
        (["vendor"] + ["in_house"] * 4, OrgSourcingMix.MOSTLY_INTERNAL),  # 0.2
        (["vendor", "in_house"], OrgSourcingMix.MIXED),  # 0.5
        # None entries are excluded, not counted as in-house.
        (["vendor", None, None], OrgSourcingMix.VENDOR_ONLY),
    ],
)
def test_org_sourcing_mix_rollup(sourcings, expected):
    assert org_sourcing_mix(sourcings) is expected


def test_org_sourcing_mix_accepts_enum_members():
    # vendor + hybrid = (1.0 + 0.5) / 2 = 0.75, which sits ON the mostly-vendor
    # threshold (> 0.75) and therefore reads MIXED.
    assert (
        org_sourcing_mix([RegistrySourcing.VENDOR, RegistrySourcing.HYBRID])
        is OrgSourcingMix.MIXED
    )


def test_org_sourcing_mix_rejects_unknown_vocabulary():
    with pytest.raises(ValueError):
        org_sourcing_mix(["third_party"])

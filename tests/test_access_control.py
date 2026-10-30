"""
Write tests here proving:
  1. A PropertyManager scoped to la-001 (pm-001) is DENIED access to la-002's tenant's
     screening report (rep-002).
  2. The same PropertyManager (pm-001) IS allowed access to their own account's screening
     report (rep-001).

Use the `property_managers`, `properties`, `tenants`, and `screening_reports` fixtures from
conftest.py — don't re-invent the seed data here.
"""
from app.access_control import can_access_screening_report
from app.models import ScreeningReport, Tenant


def test_denies_access_to_another_landlord_account(
    property_managers, properties, tenants, screening_reports
):
    assert not can_access_screening_report(
        property_managers[0],
        screening_reports[1],
        properties=properties,
        tenants=tenants,
    )


def test_allows_access_within_the_same_landlord_account(
    property_managers, properties, tenants, screening_reports
):
    assert can_access_screening_report(
        property_managers[0],
        screening_reports[0],
        properties=properties,
        tenants=tenants,
    )


def test_denies_access_when_report_tenant_is_missing(
    property_managers, properties, tenants
):
    report = ScreeningReport(
        id="rep-missing-tenant",
        tenant_id="ten-missing",
        ssn_last4="0000",
        credit_score=0,
    )

    assert not can_access_screening_report(
        property_managers[0],
        report,
        properties=properties,
        tenants=tenants,
    )


def test_denies_access_when_tenant_property_is_missing(
    property_managers, properties
):
    tenant = Tenant(id="ten-missing-property", name="Unknown", property_id="prop-missing")

    assert not can_access_screening_report(
        property_managers[0],
        ScreeningReport(
            id="rep-missing-property",
            tenant_id=tenant.id,
            ssn_last4="0000",
            credit_score=0,
        ),
        properties=properties,
        tenants=[tenant],
    )

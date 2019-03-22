from datetime import date

from django.test import TestCase

from workbench import factories
from workbench.invoices.models import RecurringInvoice


class RecurringTest(TestCase):
    def test_recurring_invoice(self):
        person = factories.PersonFactory.create(
            organization=factories.OrganizationFactory.create()
        )
        pa = factories.PostalAddressFactory.create(person=person)

        ri = RecurringInvoice.objects.create(
            customer=person.organization,
            contact=person,
            title="Recurring invoice",
            description="",
            owned_by=person.primary_contact,
            postal_address=pa.postal_address,
            starts_on=date(2018, 1, 1),
            ends_on=date(2018, 12, 31),
            periodicity="monthly",
        )

        self.assertEqual(ri.next_period_starts_on, None)

        self.assertEqual(len(ri.create_invoices(generate_until=date(2019, 1, 1))), 12)

        ri.ends_on = None
        ri.save()
        self.assertEqual(len(ri.create_invoices(generate_until=date(2019, 1, 1))), 1)

        self.assertTrue(len(RecurringInvoice.objects.create_invoices()) > 1)
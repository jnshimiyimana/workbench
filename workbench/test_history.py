import datetime as dt

from django.test import TestCase
from django.test.utils import override_settings

from workbench import factories
from workbench.accounts.features import FEATURES
from workbench.accounts.middleware import set_user_name
from workbench.projects.models import Project
from workbench.tools import history


class HistoryTest(TestCase):
    def test_header(self):
        set_user_name("ballabla")
        user1 = factories.UserFactory.create(_full_name="foo")
        set_user_name("user-%d-%s" % (user1.id, user1.get_short_name()))
        user2 = factories.UserFactory.create(_full_name="bar")
        set_user_name("user-%d-%s" % (user2.id, user2.get_short_name()))
        user3 = factories.UserFactory.create()

        self.client.force_login(user1)

        response = self.client.get("/history/accounts_user/id/{}/".format(user1.pk))
        self.assertContains(response, "INSERT accounts_user {}".format(user1.pk))

        response = self.client.get("/history/accounts_user/id/{}/".format(user2.pk))
        self.assertContains(response, "INSERT accounts_user {}".format(user2.pk))

        response = self.client.get("/history/accounts_user/id/{}/".format(user3.pk))
        self.assertContains(response, "INSERT accounts_user {}".format(user3.pk))

    def test_history(self):
        project = factories.ProjectFactory.create()
        project.owned_by = factories.UserFactory.create()
        project.type = Project.INTERNAL
        project.closed_on = dt.date(2019, 1, 1)
        project.save()

        self.client.force_login(project.owned_by)
        response = self.client.get(
            "/history/projects_project/id/{}/".format(project.pk)
        )
        # print(response, response.content.decode("utf-8"))
        self.assertContains(response, "Initial value of 'Customer' was")
        self.assertContains(response, "The Organization Ltd")

    def test_contact_history(self):
        person = factories.PersonFactory.create()
        person.is_archived = True
        person.save()
        self.client.force_login(person.primary_contact)
        response = self.client.get("/history/contacts_person/id/{}/".format(person.pk))
        # print(response, response.content.decode("utf-8"))
        self.assertContains(response, "New value of 'Is archived' was 'yes'.")

    def test_related_history(self):
        pa = factories.PostalAddressFactory.create()
        self.client.force_login(pa.person.primary_contact)
        response = self.client.get(
            "/history/contacts_postaladdress/person_id/{}/".format(pa.person_id)
        )
        # print(response, response.content.decode("utf-8"))
        self.assertContains(response, "INSERT contacts_postaladdress {}".format(pa.pk))

    def test_nothing(self):
        self.client.force_login(factories.UserFactory.create())
        response = self.client.get("/history/contacts_person/id/0/")
        # print(response, response.content.decode("utf-8"))
        self.assertContains(response, "No history found")

    def test_deleted(self):
        organization = factories.OrganizationFactory.create()
        person = factories.PersonFactory.create(organization=organization)
        person.organization = None
        person.save()
        pk = organization.pk
        organization.delete()

        self.client.force_login(factories.UserFactory.create())
        response = self.client.get("/history/contacts_person/id/{}/".format(person.pk))
        self.assertContains(
            response,
            '<a href="/history/contacts_organization/id/{}/" data-toggle="ajaxmodal">'
            "Deleted organization instance</a>".format(pk),
        )

        response = self.client.get("/history/contacts_organization/id/{}/".format(pk))
        self.assertContains(
            response, "Final value of 'Name' was 'The Organization Ltd'."
        )
        # print(response, response.content.decode("utf-8"))

    def test_exclusion(self):
        service = factories.ServiceFactory.create()
        service.position += 1
        service.save()
        service.position += 1
        service.save()
        service.title += " test"
        service.save()

        self.client.force_login(service.project.owned_by)
        response = self.client.get(
            "/history/projects_service/id/{}/".format(service.id)
        )
        self.assertContains(response, "INSERT")
        # Only two versions -- position changes are excluded
        self.assertContains(response, "UPDATE", 1)

    def test_nocrash(self):
        # Do not crash when encountering invalid values.
        self.assertEqual(history.boolean_formatter("stuff"), "stuff")
        self.assertEqual(history.date_formatter("stuff"), "stuff")

    def test_404(self):
        self.client.force_login(factories.UserFactory.create())
        response = self.client.get("/history/not_exists/id/3/")
        self.assertEqual(response.status_code, 404)

    def assert_only_visible_with(self, url, text, feature):
        with override_settings(FEATURES={feature: True}):
            response = self.client.get(url)
            self.assertContains(response, text)

        with override_settings(FEATURES={feature: False}):
            response = self.client.get(url)
            self.assertNotContains(response, text)

    def test_offer_total_visibility(self):
        offer = factories.OfferFactory.create()
        self.client.force_login(offer.owned_by)
        url = "/history/offers_offer/id/{}/".format(offer.pk)
        self.assert_only_visible_with(url, "'Total'", FEATURES.CONTROLLING)

    def test_logged_cost_visibility(self):
        cost = factories.LoggedCostFactory.create()
        self.client.force_login(cost.rendered_by)
        url = "/history/logbook_loggedcost/id/{}/".format(cost.pk)
        self.assert_only_visible_with(url, "'Archived at'", FEATURES.CONTROLLING)
        self.assert_only_visible_with(
            url, "'Original cost'", FEATURES.FOREIGN_CURRENCIES
        )

    def test_logged_hours_visibility(self):
        hours = factories.LoggedHoursFactory.create()
        self.client.force_login(hours.rendered_by)
        url = "/history/logbook_loggedhours/id/{}/".format(hours.pk)
        self.assert_only_visible_with(url, "'Archived at'", FEATURES.CONTROLLING)

    def test_project_visibility(self):
        project = factories.ProjectFactory.create()
        self.client.force_login(project.owned_by)
        url = "/history/projects_project/id/{}/".format(project.pk)
        self.assert_only_visible_with(url, "'Flat rate'", FEATURES.CONTROLLING)

    def test_project_service_visibility(self):
        service = factories.ServiceFactory.create()
        self.client.force_login(service.project.owned_by)
        url = "/history/projects_service/id/{}/".format(service.pk)
        self.assert_only_visible_with(url, "'Cost'", FEATURES.CONTROLLING)
        self.assert_only_visible_with(url, "'Role'", FEATURES.GLASSFROG)

    def assert_404_without_controlling(self, url):
        with override_settings(FEATURES={"controlling": True}):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        with override_settings(FEATURES={"controlling": False}):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)

    def test_credit_entry_visibility(self):
        self.client.force_login(factories.UserFactory.create())
        entry = factories.CreditEntryFactory.create()
        url = "/history/credit_control_creditentry/id/{}/".format(entry.pk)
        self.assert_404_without_controlling(url)

    def test_invoice_visibility(self):
        invoice = factories.InvoiceFactory.create()
        self.client.force_login(invoice.owned_by)
        url = "/history/invoices_invoice/id/{}/".format(invoice.pk)
        self.assert_404_without_controlling(url)

    def test_invoice_service_visibility(self):
        invoice = factories.InvoiceFactory.create()
        self.client.force_login(invoice.owned_by)
        service = invoice.services.create()
        url = "/history/invoices_service/id/{}/".format(service.pk)
        self.assert_404_without_controlling(url)

    def test_recurring_invoice_visibility(self):
        invoice = factories.RecurringInvoiceFactory.create()
        self.client.force_login(invoice.owned_by)
        url = "/history/invoices_recurringinvoice/id/{}/".format(invoice.pk)
        self.assert_404_without_controlling(url)

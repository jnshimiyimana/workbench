import datetime as dt

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.translation import deactivate_all

from workbench import factories


class PlanningTest(TestCase):
    def setUp(self):
        deactivate_all()

    def test_no_monday(self):
        """Non-mondays are rejected from PlannedWork.weeks"""
        pw = factories.PlannedWorkFactory.create(weeks=[dt.date(2020, 6, 21)])

        msg = ["Only mondays allowed, but field contains 21.06.2020."]

        with self.assertRaises(ValidationError) as cm:
            pw.clean_fields(exclude=["weeks"])
        self.assertEqual(list(cm.exception), msg)

        pr = factories.PlanningRequestFactory.create()
        pr.full_clean()

        pr.earliest_start_on = dt.date(2020, 6, 14)
        pr.completion_requested_on = dt.date(2020, 6, 21)

        with self.assertRaises(ValidationError) as cm:
            pr.clean_fields()

        msg = [
            ("earliest_start_on", ["Only mondays allowed."]),
            ("completion_requested_on", ["Only mondays allowed."]),
        ]
        self.assertEqual(list(cm.exception), msg)

        pr = factories.PlanningRequestFactory.create()
        pr.completion_requested_on = pr.earliest_start_on

        msg = ["Allow at least one week for the work please."]

        with self.assertRaises(ValidationError) as cm:
            pr.clean_fields(exclude=["completion_requested_on"])

        self.assertEqual(list(cm.exception), msg)

import datetime as dt
from collections import defaultdict
from itertools import islice

from workbench.accounts.models import User
from workbench.invoices.utils import recurring
from workbench.planning.models import PlannedWork
from workbench.tools.formats import Z1, Z2, local_date_format
from workbench.tools.validation import monday


def planned_work(*, users=None):
    weeks = list(islice(recurring(monday(), "weekly"), 35))

    by_week = defaultdict(lambda: Z1)
    by_project_and_week = defaultdict(lambda: defaultdict(lambda: Z1))
    projects_offers = defaultdict(lambda: defaultdict(list))

    for pw in PlannedWork.objects.filter(weeks__overlap=weeks).select_related(
        "project__owned_by", "offer__project", "offer__owned_by"
    ):
        per_week = (pw.planned_hours / len(pw.weeks)).quantize(Z2)
        for week in pw.weeks:
            by_week[week] += per_week
            by_project_and_week[pw.project][week] += per_week

        date_from = min(pw.weeks)
        date_until = max(pw.weeks) + dt.timedelta(days=6)

        projects_offers[pw.project][pw.offer].append(
            {
                "planned_work": {
                    "id": pw.id,
                    "title": pw.title,
                    "planned_hours": pw.planned_hours,
                    "update_url": pw.urls["update"],
                    "date_from": date_from,
                    "date_until": date_until,
                    "range": "{} – {}".format(
                        local_date_format(date_from, fmt="d.m."),
                        local_date_format(date_until, fmt="d.m."),
                    ),
                },
                "hours_per_week": [
                    per_week if week in pw.weeks else Z1 for week in weeks
                ],
            }
        )

    def offer_record(offer, planned_works):
        date_from = min(pw["planned_work"]["date_from"] for pw in planned_works)
        date_until = max(pw["planned_work"]["date_until"] for pw in planned_works)
        hours = sum(pw["planned_work"]["planned_hours"] for pw in planned_works)

        return {
            "offer": {
                "date_from": date_from,
                "date_until": date_until,
                "range": "{} – {}".format(
                    local_date_format(date_from, fmt="d.m."),
                    local_date_format(date_until, fmt="d.m."),
                ),
                "planned_hours": hours,
                **(
                    {
                        "id": offer.id,
                        "title": offer.title,
                        "code": offer.code,
                        "url": offer.get_absolute_url(),
                    }
                    if offer
                    else {}
                ),
            },
            "planned_works": sorted(
                planned_works,
                key=lambda row: (
                    row["planned_work"]["date_from"],
                    row["planned_work"]["date_until"],
                ),
            ),
        }

    def project_record(project, offers):
        offers = sorted(
            (
                offer_record(offer, planned_works)
                for offer, planned_works in sorted(offers.items())
            ),
            key=lambda row: (
                row["offer"]["date_from"],
                row["offer"]["date_until"],
                -row["offer"]["planned_hours"],
            ),
        )

        date_from = min(rec["offer"]["date_from"] for rec in offers)
        date_until = max(rec["offer"]["date_until"] for rec in offers)
        hours = sum(rec["offer"]["planned_hours"] for rec in offers)

        return {
            "project": {
                "id": project.id,
                "title": project.title,
                "code": project.code,
                "url": project.get_absolute_url(),
                "date_from": date_from,
                "date_until": date_until,
                "range": "{} – {}".format(
                    local_date_format(date_from, fmt="d.m."),
                    local_date_format(date_until, fmt="d.m."),
                ),
                "planned_hours": hours,
            },
            "by_week": [by_project_and_week[project][week] for week in weeks],
            "offers": offers,
        }

    return {
        "weeks": [
            {
                "date_from": week,
                "date_until": week + dt.timedelta(days=6),
                "week": local_date_format(week, fmt="W"),
            }
            for week in weeks
        ],
        "projects_offers": sorted(
            [
                project_record(project, offers)
                for project, offers in projects_offers.items()
            ],
            key=lambda row: (
                row["project"]["date_from"],
                row["project"]["date_until"],
                -row["project"]["planned_hours"],
            ),
        ),
        "by_week": [by_week[week] for week in weeks],
    }


def test():  # pragma: no cover
    from pprint import pprint

    pprint(planned_work(users=[User.objects.get(pk=1)]))

    # pprint(accepted_deals([dt.date(2020, 1, 1), dt.date(2020, 3, 31)]))

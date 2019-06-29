from collections import defaultdict

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext as _

from workbench.invoices.models import RecurringInvoice
from workbench.tools.formats import currency, local_date_format


def create_recurring_invoices_and_notify():
    by_owner = defaultdict(list)
    for invoice in RecurringInvoice.objects.create_invoices():
        by_owner[invoice.owned_by].append(invoice)

    for owner, invoices in by_owner.items():
        invoices = "\n".join(
            "{} {} {}\n{}{}\n".format(
                invoice,
                currency(invoice.total),
                local_date_format(invoice.invoiced_on, "d.m.Y"),
                settings.WORKBENCH.URL,
                invoice.get_absolute_url(),
            )
            for invoice in invoices
        )
        mail = EmailMultiAlternatives(
            _("recurring invoices"),
            invoices,
            to=[owner.email],
            bcc=[row[1] for row in settings.MANAGERS],
        )
        mail.send()
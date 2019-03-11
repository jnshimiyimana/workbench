from django.db import models
from django.utils.translation import gettext_lazy as _

from workbench.invoices.models import Invoice
from workbench.tools.models import Model, MoneyField, SearchQuerySet
from workbench.tools.urls import model_urls


class CreditEntryQuerySet(SearchQuerySet):
    pass


@model_urls()
class CreditEntry(Model):
    reference_number = models.CharField(
        _("reference number"), max_length=40, unique=True
    )
    value_date = models.DateField(_("value date"))
    total = MoneyField(_("total"))
    payment_notice = models.CharField(_("payment notice"), max_length=1000, blank=True)

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="+",
        verbose_name=_("invoice"),
    )
    notes = models.TextField(_("notes"), blank=True)

    objects = CreditEntryQuerySet.as_manager()

    class Meta:
        ordering = ["-value_date", "-pk"]
        verbose_name = _("credit entry")
        verbose_name_plural = _("credit entries")

    def __str__(self):
        return self.reference_number
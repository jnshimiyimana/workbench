from django.conf.urls import url

from workbench import generic
from workbench.accounts.features import controlling_only
from workbench.invoices.forms import RecurringInvoiceForm, RecurringInvoiceSearchForm
from workbench.invoices.models import RecurringInvoice
from workbench.invoices.views import RecurringInvoiceDetailView


urlpatterns = [
    url(
        r"^$",
        controlling_only(
            generic.ListView.as_view(
                model=RecurringInvoice, search_form_class=RecurringInvoiceSearchForm
            )
        ),
        name="invoices_recurringinvoice_list",
    ),
    url(
        r"^(?P<pk>\d+)/$",
        controlling_only(RecurringInvoiceDetailView.as_view(model=RecurringInvoice)),
        name="invoices_recurringinvoice_detail",
    ),
    url(
        r"^create/$",
        controlling_only(
            generic.CreateView.as_view(
                model=RecurringInvoice, form_class=RecurringInvoiceForm
            )
        ),
        name="invoices_recurringinvoice_create",
    ),
    url(
        r"^(?P<pk>\d+)/update/$",
        controlling_only(
            generic.UpdateView.as_view(
                model=RecurringInvoice, form_class=RecurringInvoiceForm
            )
        ),
        name="invoices_recurringinvoice_update",
    ),
    url(
        r"^(?P<pk>\d+)/delete/$",
        controlling_only(generic.DeleteView.as_view(model=RecurringInvoice)),
        name="invoices_recurringinvoice_delete",
    ),
]

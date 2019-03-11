from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


default_app_config = "workbench.credit_control.Config"


class Config(AppConfig):
    name = "workbench.credit_control"
    verbose_name = _("credit control")
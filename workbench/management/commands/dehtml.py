from html.parser import HTMLParser
import re

from django.core.management.base import BaseCommand

from workbench.invoices.models import Invoice
from workbench.offers.models import Offer
from workbench.projects.models import Project, Service


class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = re.sub("[ \t\r\n]+", " ", text)
            self.__text.append(text + " ")

    def handle_entityref(self, name):
        self.__text.append(self.unescape("&%s;" % name))

    def handle_charref(self, name):
        self.__text.append(self.unescape("&#%s;" % name))

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self.__text.append("\n\n")
        elif tag == "br":
            self.__text.append("\n")
        elif tag == "li":
            self.__text.append("\n- ")

    def handle_startendtag(self, tag, attrs):
        if tag == "br":
            self.__text.append("\n\n")

    def text(self):
        return "".join(self.__text).strip()


def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except Exception:
        return text


class Command(BaseCommand):
    help = "De-htmlizes description fields"

    def handle(self, **options):
        self.stdout.write("dehtmling invoices...")
        for instance in Invoice.objects.all():
            instance.description = dehtml(instance.description)
            instance.save(update_fields=("description",))
        self.stdout.write("dehtmling offers...")
        for instance in Offer.objects.all():
            instance.description = dehtml(instance.description)
            instance.save(update_fields=("description",))
        self.stdout.write("dehtmling projects...")
        for instance in Project.objects.all():
            instance.description = dehtml(instance.description)
            instance.save(update_fields=("description",))
        self.stdout.write("refreshing services...")
        for idx, service in enumerate(
            Service.objects.prefetch_related("efforts__service_type", "costs")
        ):
            if idx % 250 == 0:
                print("processed %s services" % idx)
            service.save()

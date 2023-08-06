from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import models


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("find")
        parser.add_argument("replace")
        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_false",
            dest="interactive",
            default=True,
            help="Tells Django to NOT prompt the user for input of any kind.",
        )

    def handle(self, *args, **options):
        if options["interactive"]:
            self.stdout.write(
                '\nReplace ALL instances of "{}" with "{}"?\n\n'.format(
                    options["find"], options["replace"]
                )
            )
            confirm = input("    Type 'yes' to continue, or 'no' to cancel: ")
        else:
            confirm = "yes"

        updated_count = 0

        if confirm == "yes":
            for field in self.get_fields():
                updated_count += self.find_replace(
                    field=field, find=options["find"], replace=options["replace"]
                )
        else:
            self.stdout.write("Find and replace cancelled.")

    def find_replace(self, field, find, replace):
        updated_count = 0
        model = field.model
        filter_kwargs = {"{}__contains".format(field.name): find}

        # To avoid signals at all costs, we have to:
        # - Use values_list to avoid pre/post init
        # - Use update to avoid pre/post save
        queryset = model._default_manager.filter(**filter_kwargs).values_list("pk", field.name)
        for pk, field_data in queryset.iterator():
            update_kwargs = {field.name: field_data.replace(find, replace)}
            updated_count += model._default_manager.filter(pk=pk).update(**update_kwargs)

        return updated_count

    def get_fields(self):
        """
        Return a list of fields from installed apps which can be updated.

        Any registered models with fields which extend from CharField or TextField will be returned
        as a list of fields.
        """
        fields = []

        for app in apps.get_app_configs():
            for model in app.get_models():
                for field in model._meta.get_fields():
                    if isinstance(field, (models.CharField, models.TextField)):
                        fields.append(field)

        return fields

import csv
from django.http import HttpResponse

def export_as_csv_action(description="Export selected objects as CSV", fields=None, exclude=None, header=True):
    """
    This function returns an export action for Django Admin.
    """
    def export_as_csv(modeladmin, request, queryset):
        # Set the response
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{modeladmin.model._meta.verbose_name_plural}.csv"'
        writer = csv.writer(response)

        # Define fields to export
        opts = modeladmin.model._meta
        field_names = fields or [field.name for field in opts.fields]

        # Write the CSV header
        if header:
            writer.writerow(field_names)

        # Write the CSV data
        for obj in queryset:
            row = [getattr(obj, field) for field in field_names]
            writer.writerow(row)

        return response

    export_as_csv.short_description = description
    return export_as_csv

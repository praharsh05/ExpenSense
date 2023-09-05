from datetime import datetime, timedelta
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_start_and_end_dates(context, report):
    try:
        # Parse the input string into a datetime object
        report_date = datetime.strptime(report, "%B %Y")

        # Calculate the start date (first day of the month)
        start_date = report_date.strftime("%Y-%m-01")

        # Calculate the end date (last day of the month)
        end_date = report_date.strftime("%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d").replace(day=1, month=report_date.month % 12 + 1) - timedelta(days=1)
        end_date = end_date.strftime("%Y-%m-%d")

        # Set the results in the context variables
        context['start_date'] = start_date
        context['end_date'] = end_date
    except ValueError:
        # Return empty strings if the input format is invalid
        context['start_date'] = ""
        context['end_date'] = ""
    return ''  # Always return an empty string from the simple_tag
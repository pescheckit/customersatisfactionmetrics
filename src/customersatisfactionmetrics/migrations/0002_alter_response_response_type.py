"""
Django migration to alter the 'response_type' field in the 'response' model.

This migration changes the choices and max_length of the 'response_type' field
in the 'response' model within the Customer Satisfaction Metrics application.
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Migration class for altering the 'response_type' field in the 'response' model.

    Modifies the 'response_type' field to adjust the choices and max_length to
    accommodate different types of responses.
    """

    dependencies = [
        ("customersatisfactionmetrics", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="response",
            name="response_type",
            field=models.CharField(
                choices=[
                    ("CSAT", "Customer Satisfaction"),
                    ("NPS", "Net Promoter Score"),
                    ("CES", "Customer Effort Score"),
                    ("GENERIC", "Generic Survey"),
                ],
                max_length=22,
            ),
        ),
    ]

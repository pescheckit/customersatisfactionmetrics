"""
Django migration for altering the 'question' model options and adding the 'order' field.

This migration updates the 'question' model within the Customer Satisfaction Metrics application,
setting the 'ordering' option and adding a new 'order' field to the model.
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Migration class for altering the 'question' model options and adding the 'order' field.

    This class handles the modification of the model's meta options and the addition
    of the 'order' field to the 'question' model.
    """

    dependencies = [
        ("customersatisfactionmetrics", "0002_alter_response_response_type"),
    ]

    operations = [
        migrations.AlterModelOptions(name="question", options={"ordering": ["order"]},),
        migrations.AddField(
            model_name="question", name="order", field=models.IntegerField(default=0),
        ),
    ]

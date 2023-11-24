"""
Django migration for adding the 'is_required' field to the 'question' model.

This migration introduces a new boolean field 'is_required' to the 'question' model
in the Customer Satisfaction Metrics application, with a default value of True.
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Migration class for adding the 'is_required' field to the 'question' model.

    Handles the addition of the 'is_required' boolean field to the 'question' model,
    specifying whether a response to the question is required or not.
    """

    dependencies = [
        ("customersatisfactionmetrics", "0003_alter_question_options_question_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="is_required",
            field=models.BooleanField(default=True),
        ),
    ]

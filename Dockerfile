FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /code/

# Install the local package
COPY customersatisfactionmetrics /code/customersatisfactionmetrics

# Install pipenv and dependencies
RUN pip install pipenv && pipenv install --system --deploy

RUN pip install /code/customersatisfactionmetrics

# Ensure Django is installed as part of the dependencies before this step
# Create the Django app
RUN mkdir /code/customer_satisfaction_metrics
RUN django-admin startapp customer_satisfaction_metrics /code/customer_satisfaction_metrics

# Copy other necessary files
COPY manage.py /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
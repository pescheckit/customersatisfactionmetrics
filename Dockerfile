FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /code/

# Copy the Django app and the locally developed package
COPY customer_satisfaction_metrics /code/customer_satisfaction_metrics
COPY customersatisfactionmetrics /code/customersatisfactionmetrics

# Install pipenv and dependencies
RUN pip install pipenv && pipenv install --system --deploy

# Install the local package
RUN pip install /code/customersatisfactionmetrics

# Copy other necessary files
COPY manage.py /code/
# Copy any other required files or directories

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /code/

# Install the local package
COPY src/customersatisfactionmetrics /code/src/customersatisfactionmetrics
COPY customer_satisfaction_metrics /code/customer_satisfaction_metrics

# Install pipenv and dependencies
RUN pip install pipenv
RUN pipenv install --system --deploy

RUN pipenv install ./src/customersatisfactionmetrics

# Copy other necessary files
COPY manage.py /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Django Survey App

This Django application allows you to create and manage surveys including CSAT, NPS, CES, and Generic Surveys. It supports both anonymous and logged-in user responses with user metadata tracking.

## Setup and Installation

### 1. Install the Application

To install the `customersatisfactionmetrics` package, run the following command:

```bash
pip install customersatisfactionmetrics
```

### 2. Update Django Settings

Add `customersatisfactionmetrics` to the `INSTALLED_APPS` list in your Django project's `settings.py` file:

```python
INSTALLED_APPS = [
    # ... other installed apps ...
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "customersatisfactionmetrics",  # Add this line
]
```

### 3. Run Migrations

Apply the necessary migrations to your database with the following command:

```bash
python manage.py migrate
```

### 4. Run the Django Server

Start the Django development server:

```bash
python manage.py runserver
```

Access the admin panel at [http://localhost:8000/admin/](http://localhost:8000/admin/).

### 5. Adding Surveys and Questions

- Navigate to the Django admin site.
- Use the respective sections to add new surveys and questions.

### 6. URL Configuration

Include the `customersatisfactionmetrics` URLs in your project's `urls.py` file:

```python
from django.urls import path, include

urlpatterns = [
    path('', include('customersatisfactionmetrics.urls')),
    # ... other URL patterns ...
]
```

## Usage

### 1. Access the Survey

To view a survey, navigate to the URL path `survey/slug/<slug>` in your web browser, where `<slug>` is the slug you assigned to the survey in the admin panel. For example:

```
http://localhost:8000/survey/slug/sample-survey
```

This URL will display the survey form for users to fill out and submit.


### 2. Embedding Surveys in Templates

To easily embed a survey in your Django templates, you can use the `insert_survey_by_slug` template tag. This tag allows you to insert a survey form by its slug directly into a template.

First, load the template tag in your template file:

```html
{% load survey_tags %}
```

Then, use the `insert_survey_by_slug` tag to insert a survey form by specifying its slug:

```html
{% insert_survey_by_slug 'your-survey-slug' %}
```

Replace `'your-survey-slug'` with the actual slug of the survey you want to embed. The survey form will be rendered wherever you include this tag in your template.

Example:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Survey Page</title>
</head>
<body>
    <h1>Survey Form</h1>
    {% load survey_tags %}
    {% insert_survey_by_slug 'sample-survey' %}
</body>
</html>
```

This method provides a flexible way to integrate surveys into various parts of your Django application without the need for additional view logic or URL configurations.


## Features

- Supports various survey types: CSAT, NPS, CES, and Generic.
- Allows both anonymous and logged-in user responses.
- Tracks user metadata like IP address and user agent.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request.

## License

This project is licensed under [MIT License](LICENSE). See the [LICENSE](LICENSE) file in the respective folders for more details.

## Contact

For any queries or further information, please contact us at devops@pescheck.nl.

Thank you for your interest in our Django Survey Project!

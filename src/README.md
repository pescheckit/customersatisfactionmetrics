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


### 3. Touchpoints: asking only sometimes

`insert_survey_by_slug` renders a survey every single time the template is
rendered. A **touchpoint** wraps a survey in rules about *when* it may be shown,
so you can leave the tag in a shared template and trust that visitors are not
asked repeatedly.

Create a `Touchpoint` in the admin, point it at a survey, then render it:

```html
{% load survey_tags %}
{% survey_touchpoint 'order-placed' %}
```

This renders nothing at all when the touchpoint does not exist, is inactive, or
the visitor is inside a cooldown, so it is safe to place on any page. Rendering
it records an `Impression`, which is what the cooldown is measured against and
what lets you compute a real response rate later.

The tag needs `django.template.context_processors.request` enabled.

#### Cooldowns

Each touchpoint carries its own rules:

| Field | Meaning |
| --- | --- |
| `cooldown_days` | How long a respondent is left alone after being shown a survey. Defaults to 84 days (12 weeks). |
| `cooldown_scope` | `GLOBAL` means being shown *any* touchpoint starts the cooldown for all of them; `TOUCHPOINT` confines it to this one. Defaults to `GLOBAL`. |
| `scope_cooldown_days` | An optional second cooldown applied to a shared scope key, so a whole team or tenant is not surveyed in the same week. `0` disables it. |
| `is_active` | Pause a touchpoint without touching code. |

An impression that is neither answered nor dismissed stays reusable for
`SURVEY_OPEN_IMPRESSION_TTL_HOURS` (24 by default). Within that window a page
reload shows the same card again rather than it silently vanishing, and no
second impression is recorded. After it, the impression counts as ignored.

#### Scope keys

A scope key is an opaque string that groups respondents, typically an
organisation or tenant id. Pass it explicitly:

```html
{% survey_touchpoint 'order-placed' scope_key=organisation.scope_key %}
```

Or configure a resolver once and let the package call it:

```python
# settings.py
SURVEY_SCOPE_RESOLVER = "myapp.utils.current_organisation_key"
```

```python
# myapp/utils.py
def current_organisation_key(request):
    organisation = getattr(request, "organisation", None)
    return f"org:{organisation.id}" if organisation else ""
```

The package never imports your models; it only ever sees the string you return.

#### Measuring

Because impressions are recorded separately from responses, you can distinguish
"never asked" from "asked and ignored":

```python
from customersatisfactionmetrics.models import Impression

shown = Impression.objects.filter(touchpoint__slug="order-placed")
response_rate = shown.filter(responded_at__isnull=False).count() / shown.count()
```

#### Linking feedback to an object

Knowing *who* answered is often not enough, and sometimes impossible: a visitor
filling in a public form has no user account at all. Every `Response` and
`Impression` can therefore point at any object in your application through a
generic relation, so an answer stays traceable to the thing it was about.

Pass it to the tag:

```html
{% survey_touchpoint 'order-placed' subject=order %}
```

The subject is stored on the impression and the answers **inherit it on
submission**, read back from the impression rather than posted with the form, so
a respondent cannot relabel their feedback as being about somebody else's
object.

For a survey rendered outside a touchpoint, pass it when processing the form:

```python
from customersatisfactionmetrics.views.survey_view import process_form_submission

process_form_submission(request, form, survey, subject=order)
```

Then query it back:

```python
from customersatisfactionmetrics.models import Response, subject_filter

Response.objects.filter(**subject_filter(order))
```

Primary keys are stored as text, so integer, UUID and slug primary keys all
work. The subject is optional, and deleting the object it points at leaves the
answer readable: the recorded `content_type` and `object_id` survive.

This requires `django.contrib.contenttypes` in `INSTALLED_APPS`, which Django
enables by default.


#### Ratings with a comment

A scored survey (`CSAT`, `NPS`, `CES`) fixes the bounds of its `INT` questions
(1-5, or 0-10 for NPS) but leaves `TEXT` and `BOOL` questions alone. That is what
lets a short survey pair a rating with an optional comment, which is the usual
shape of an in-product survey: one required score, one optional free text.

Marking the comment optional matters. Requiring free text is the single most
common reason in-product surveys collect almost nothing.


## Features

- Supports various survey types: CSAT, NPS, CES, and Generic.
- Allows both anonymous and logged-in user responses.
- Tracks user metadata like IP address and user agent.
- Touchpoints with per respondent and per scope cooldowns, so surveys are shown
  only sometimes rather than on every page render.
- Impression tracking, which distinguishes "never asked" from "asked and
  ignored" and makes a real response rate computable.
- Generic subject links, so a response can be tied to any object in your
  application even when the respondent is anonymous.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request.

## License

This project is licensed under [MIT License](LICENSE). See the [LICENSE](LICENSE) file in the respective folders for more details.

## Contact

For any queries or further information, please contact us at devops@pescheck.nl.

Thank you for your interest in our Django Survey Project!

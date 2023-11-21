# Django Survey App

This Django application allows you to create and manage surveys including CSAT, NPS, CES, and Generic Surveys. It supports both anonymous and logged-in user responses with user metadata tracking.

## Setup and Installation

1. **Run Migrations**

   ```
   python manage.py migrate
   ```

2. **Run Server**

   ```
   python manage.py runserver
   ```

   Access the admin panel at `http://localhost:8000/admin/`.

3. **Adding Surveys and Questions**

   - Navigate to the Django admin site.
   - Add new surveys and questions under the respective sections.

4. **URL Configuration**

   Include survey-related URLs in your project's `urls.py` file. Example:
   ```python
   from django.urls import path, include

   urlpatterns = [
       path('', include('customersatisfactionmetrics.urls')),
       # ... other URL patterns
   ]
   ```


## Features

- Supports various survey types: CSAT, NPS, CES, and Generic.
- Allows both anonymous and logged-in user responses.
- Tracks user metadata like IP address and user agent.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request.

## License

[Your chosen license]

## Contact

[Your contact information]



# Django Survey Project

Welcome to the Django Survey Project! This repository hosts a collection of Django applications and tools, including our feature-rich Django Survey App. Our goal is to provide a robust and flexible solution for creating and managing various types of surveys.

## Project Structure

This project is structured as follows:

- **Django Survey App**: A Django application for creating and managing surveys, including CSAT, NPS, CES, and Generic Surveys. It's designed to support both anonymous and logged-in user responses, with comprehensive user metadata tracking. [Read more about the Django Survey App](src/customersatisfactionmetrics/README.md).

## Getting Started

**Docker Compose Integration**

In addition to the standard setup, our Django Survey Project supports Docker Compose for easy and efficient deployment. With Docker Compose, you can quickly start the entire project on your local machine or a server, simplifying the process of development and testing.

### Starting with Docker Compose

To start the project using Docker Compose, follow these steps:

1. Ensure you have Docker and Docker Compose installed on your system. If not, you can download and install them from [Docker's official website](https://www.docker.com/get-started).

2. Clone the repository (if you haven't already):
   ```bash
   git clone git@github.com:pescheckit/customersatisfactionmetrics.git
   ```

3. Navigate to the root directory of the project where the `docker-compose.yml` file is located.

4. Create a sqlite3 file:
   ```bash
   touch db.sqlite3
   ```

5. Run the following command to start the services defined in the `docker-compose.yml` file:
   ```bash
   docker compose up
   ```

6. Run the migrations:
   ```bash
   docker compose exec web python manage.py migrate
   ```

7. Once the services are up and running, you can access the Django Survey App in your browser. Typically, it will be hosted at `http://localhost:8000` or a similar local address (check your Docker Compose logs for the exact URL).

## Features

- **Diverse Survey Types**: Support for various survey types including CSAT, NPS, CES, and Generic Surveys.
- **User Response Tracking**: Capability to handle both anonymous and logged-in user responses, along with user metadata like IP address and user agent.

## Contributing

We warmly welcome contributions to the Django Survey Project! If you're interested in contributing, please:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

Please read through the individual README files of each component for specific guidelines on contributing to them.

## License

This project is licensed under [MIT License](LICENSE). See the [LICENSE](LICENSE) file in the respective folders for more details.

## Contact

For any queries or further information, please contact us at devops@pescheck.nl.

Thank you for your interest in our Django Survey Project!

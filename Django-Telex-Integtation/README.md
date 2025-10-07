# Django-Jira Integration

This is a Django REST Framework (DRF) application that provides RESTful API endpoints for Telex Interval integration that sends pending and resolved jira tasks for the week.

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
  - [Running Unit Tests](#running-unit-tests)
  - [Manual Testing](#manual-testing)
- [Deployment](#deployment)

## Introduction
This is a telex integration that uses the JIRA API endpoint to pull issues from a particular period of time in a week and send those
jira issues to telex. This process will enable teams to have an overview of pending and resolved issues from the past week, thus
enhancing productivity

Architectural diagram
![](https://github.com/telexintegrations/Django-Jira-Integration/blob/master/assets/_-%20visual%20selection.png)

1. The first step is to go [altlassian website](https://id.atlassian.com/manage-profile/security/api-tokens) to generate your API token
![](https://github.com/telexintegrations/Django-Jira-Integration/blob/master/assets/img_1.png)

2. Next, is to use the generated API token in your DRF application to pull the jira issues from the jira board
3. Go to [Telex website](https://telex.im) create and login to your account. Create a telex channel
4. Click on your created channel to copy the telex webhook url.
![](https://github.com/telexintegrations/Django-Jira-Integration/blob/master/assets/img_2.png)
![](https://github.com/telexintegrations/Django-Jira-Integration/blob/master/assets/img_3.png)

## Prerequisites

Before setting up this project, you should have the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- Git


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/telexintegrations/Django-Jira-Integration.git
   cd Telex-test
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root directory with the following variables:
   ```
   JIRA_API_TOKEN=jira-api-token
   TELEX_RETURN_URL=telex-webhook-url
   ```

2. Apply database migrations:
   ```bash
   python manage.py migrate
   ```


## Running the Application

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Access the API at http://127.0.0.1:8000/api/
3. Access the admin interface at http://127.0.0.1:8000/admin/

## API Documentation

This project uses drf-spectacular for API documentation.

1. View the Swagger UI documentation:
   ```
   http://127.0.0.1:8000/swagger/
   ```

## Testing

### Running Unit Tests

1. Run all tests:
   ```bash
   python manage.py test
   ```

2. Run tests for a specific app:
   ```bash
   python manage.py test 
   ```

### Using Curl to test the integration.json endpoint
```bash
curl --location 'https://django-jira-integration.onrender.com/integration.json/' | json_pp

```


### Using Curl to test the tick endpoint
```bash
curl --location 'https://django-jira-integration.onrender.com/tick' \
--header 'Content-Type: application/json' \
--data '{
    "channel_id": "01952d3a-2bbc-76f6-ac5c-931ece485e1b",
    "return_url": "https://ping.telex.im/v1/return/01952d3a-2bbc-76f6-ac5c-931ece485e1b",
    "settings": [
      {
        "label": "interval",
        "type": "dropdown",
        "required": True,
        "default": "* * * * *",
        "description": "Select different intervals to send message to telex channel",
        "options": ["* * * * *", "59 11 * * 6", "1 * * * *"]
      }
    ]
}'
```

## Deployment

1. Set up a production-ready web server (Nginx, Apache)
2. Configure Gunicorn or uWSGI as the WSGI server
3. Configure environment variables for production settings
4. Use a process manager like Supervisor to keep the application running


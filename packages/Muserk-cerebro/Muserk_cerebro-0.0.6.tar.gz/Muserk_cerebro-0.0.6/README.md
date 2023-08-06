# Cerebro

Cerebro is a distributed-computing management system that facilitates data management pipelines.

### Job Definitions
Pipelines are defined by Job Definitions. The purpose of the Job Definition is to store metadata universal to all running instances of the pipeline (Jobs). A Job Definition can be thought of as a collection of Task Definitions.

### Jobs
A Job is a running instance of a Job Definition. The Job keeps data universal to all running units of work (Tasks).

### Task Definitions
Units of work are defined by Task Definitions. The purpose of the Task Definition is to store metadata universal to all running units of work (Tasks).

### Tasks
A Task is a running instance of a Task Definition. The state of the related worker is kept here.

## A Note About arguments
When starting a task the arguments are derived from 4 separate places: The Task Definition, the Job, the Task, and the output of the previous task. These will all get merged into a single dictionary and passed to the message queue upon start. The arguments defined in the Task Definition will be applied to all Tasks when they are ran, the arguments defined in the Job will be applied to every task in the Job, the arguments defined in the Task will only be applied to that task and likewise with the arguments from the output of the previous Task.

Arguments can be passed into the respective API endpoints via the body of the POST.

## Getting Started

A version of the project can be ran locally with `docker-compose -f docker-compose.local.yml up`

A version of the project can be ran against remote database and message queue instances with `docker-compose up` and passing in the environment variables outlined in `docker-compose.yml`

## Running the tests

Coming soon

## Code Quality

This project is analyzed with SonarQube to standardize code style as well as detect code smells, bugs, and vulnerabilities.

## Continuous Integration

Tests, analysis, and delivery are autmated via Jenkins. This is configured via the Jenkinsfile

## Deployment

Add additional notes about how to deploy this on a live system

## Dependencies

Flask - http://flask.pocoo.org/
SQLAlchemy - https://www.sqlalchemy.org/
Marshmallow - https://marshmallow.readthedocs.io/
uWSGI - https://uwsgi-docs.readthedocs.io/en/latest/
Celery - http://www.celeryproject.org/
RabbitMQ - https://www.rabbitmq.com/
PostgreSQL - https://www.postgresql.org/
Jenkins - https://jenkins.io/
SonarQube - https://www.sonarqube.org/
Docker - https://www.docker.com/

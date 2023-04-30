<h1 align="center">CRON2.0</h1>
CRON2.0 is an advanced scheduler application that simplifies the process of scheduling cron jobs and provides a reliable error notification system. With CRON2.0, users can easily schedule their cron jobs based on specific dates and times, or set up recurring schedules such as every minute, hour, or day.

One of the standout features of CRON2.0 is its seamless integration with the Kafka messaging system. This allows the application to be distributed, making it possible for multiple consumers to subscribe to the same data stream. This feature enables the application to scale quickly and effortlessly by adding more consumers, making it a fantastic choice for enterprise environments that require high availability and fault-tolerance.

In addition to its integration with Kafka, CRON2.0 has a robust error notification system that alerts users via email in case of any issues during job execution. This feature ensures that users are informed of any errors promptly, enabling them to take the appropriate corrective action quickly.

## Features
- Easy setup: With CRON2.0, you no longer have to set up cron jobs manually, saving you time and reducing the risk of errors.
- Advanced scheduling options: The application allows users to specify the frequency of the cron job, as well as the specific time and day of the week when the job should run.
- Error notifications: In case of any errors during job execution, CRON2.0 sends email notifications to alert users so they can take appropriate action.
- Authentication system: The application includes an authentication system to ensure that only authorized users can access the scheduler, making it a secure choice for enterprise environments.

## Technology Stack
CRON2.0 is built using the following technologies:

- Python programming language
- FastAPI web framework
- MongoDB database
- Kafka messaging system
- Docker

## API Endpoints
- `POST /v1/cron-jobs`

Creates a new cron job. Requires authentication.

Examples: 
1) This schedules a cron job to be run every Sunday by 9:45 am timezone: US/Eastern
```
Headers:
Authorization: Bearer <token>

Body:
{
     "url": "https://example.com", // URL/endpoint to the cron job you want to be run 
     "method": "get", // HTTP method of your URL/endpoint
     "timezone":"US/Eastern",  // Timezone in which you want the job to run
     "weekday":"SUN", // Day of the week on which the job should run
     "hours":"9", // Hour of the day when the job should run
     "minutes":"45", // Minute of the hour when the job should run
     "notify_on_error": true // Whether to send error notifications if the job encounters an error
} 

```
2) This schedules a cron job to be run every day by 12:00 am timezone: Africa/Lagos
```
Headers:
Authorization: Bearer <token>

Body:
{
     "url": "https://example.com", // URL/endpoint to the cron job you want to be run 
     "method": "get", // HTTP method of your URL/endpoint
     "timezone":"Africa/Lagos",  // Timezone in which you want the job to run
     "days":1, // Number of days when the cron job should run
     "hours":"00", // Hour of the day when the job should run
     "minutes":"00", // Minute of the hour when the job should run
     "notify_on_error": true // Whether to send error notifications if the job encounters an error
} 

```

3) This schedules a cron job to be run every 2 hour 30 minutes timezone: Africa/Lagos
```
Headers:
Authorization: Bearer <token>

Body:
{
     "url": "https://example.com", // URL/endpoint to the cron job you want to be run 
     "method": "get", // HTTP method of your URL/endpoint
     "timezone":"Africa/Lagos",  // Timezone in which you want the job to run
     "hours":"2", // Hour of the day when the job should run
     "minutes":"30", // Minute of the hour when the job should run
     "notify_on_error": true // Whether to send error notifications if the job encounters an error
} 

```

- `GET /v1/cron-jobs`

Returns a list of all cron jobs. Requires authentication.

- `GET /v1/cron-jobs/{cron_id}`

Returns a specific cron job by ID. Requires authentication.

- `PUT /v1/cron-jobs/{cron_id}`

Updates an existing cron job by ID. Requires authentication.

- `DELETE /v1/cron-jobs/{cron_id}`

Deletes a specific cron job by ID. Requires authentication. 

- `GET /v1/response/history/{cron_id}`

Returns the response history for a specific cron job. Requires Authentication. 

- `DELETE /v1/response/history/{cron_id}`

Deletes the response history for a specific cron job. Requires Authentication. 

- `GET /v1/response/{response_id}`

Returns a specific response by ID. Requires Authentication. 

- `DELETE /v1/response/{response_id}`

Deletes a specific response by ID. Requires authentication. 
 


- `GET /v1/user`

Returns information about the authenticated user. Requires Authentication. 

- `POST /v1/signup`

Creates a new user account
```
Request Body:
{
"email": "CRON2.0@gmail.com",
"fullname": "CRON2.0", 
"password": "******" 
} 
```

- POST `/v1/login`

Authenticates a user and generates an access token that can be used to access protected resources. 

- `POST /v1/logout`

Invalidates the access token for the current user, logging them out of the system. 

## Installation and Usage
To use CRON2.0, follow these steps:

Clone the repository from GitHub
```
https://github.com/Stonetech66/CRON2.0.git
```
Install Docker and Docker Compose on your machine

Create a .env file in the root directory and populate it with the necessary environment variables. An example of the variables needed is provided in the .env.example file.

Build and start the Docker containers using the following command:
```
docker compose up 
```
Access the API docs through `http://localhost/docs` .

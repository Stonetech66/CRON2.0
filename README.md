<h1 align="center">CRON2.0</h1>
CRON2.0 is a scheduler application that automates the scheduling of cron jobs and also provides error notifications via email. With CRON2.0, users can schedule their cron jobs easily and conveniently. Users can specify the frequency of the cron job, such as every minute, hour, or day, as well as the specific time and day of the week. The application also includes an authentication system to ensure that only authorized users can access the scheduler.

One of the key benefits of this application is that it removes the stress of developers having to set up cron jobs manually, which can be time-consuming and error-prone. With this scheduler, developers can automate the process of scheduling cron jobs, freeing up their time to focus on other critical tasks.

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

Example: This schedules a cron job to be ran every Sunday by 9:45 am timezone: Africa/Lagos
```
Headers:
Authorization: Bearer <token>

Body:
{
     "url": "https://example.com", // url/endpoint to the cron job you want to be run 
     "method": "get", //the HTTP method of your url/endpoint
     "timezone":"Africa/Lagos", 
     "weekday":"SUN", 
     "hours":"9",
     "minutes":"45",
     "notify_on_error": true
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
 


- GET /v1/user

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
docker-compose up --build
```
Access the API docs through `http://localhost/docs` .

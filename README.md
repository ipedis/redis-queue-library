#### Introduction

You will need to add following env variables in your .env file for this library to be able to connect to redis.
```dotenv
REDIS_HOST=string
REDIS_PORT=int
REDIS_PASSWORD=string
REDIS_USERNAME=string
REDIS_SSL=boolean (default false)
REDIS_SSL_CA_CERT=string
```

#### Usage

Check the demo folder for the usage of the library. You can run the docker-compose file to see the demo of the package. The docker-compose file is available in the root directory of the project.
You should see the following output in the console.  
`Received message from test_channel: {'data': 'Hello World!'}`
```bash
docker-compose up
```
#### Tests
You can run test from poetry shell. Make sure you have installed the dependencies.
```bash
poetry run pytest
```
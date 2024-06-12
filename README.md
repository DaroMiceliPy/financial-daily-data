# financial-daily-data

This project is about a simple integration between terraform, python and localstack.
Basically the python script donwloads financial data of the last day and stores it into a s3 bucket.
With terraform we can deploy the s3 bucket and the dynamodb table that has information if the process
run successfully or not.


### Important

**Previous Steps...**
- You need to install [Docker and Docker Compose](https://docs.docker.com/install/) to play this game :wink:
- You can install Localstack desktop https://docs.localstack.cloud/user-guide/tools/localstack-desktop/ for see the bucket and the dynamodb table via interface.
- Just run `docker-compose up --build`

# financial-daily-data

This project is about a simple integration between terraform, python and localstack.
Basically the python script donwloads financial data of the last day and stores it into a s3 bucket.
With terraform we can deploy the s3 bucket and the dynamodb table that has information if the process
run successfully or not.

We can do: docker compose up --build

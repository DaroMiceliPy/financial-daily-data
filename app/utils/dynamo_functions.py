import os
import boto3

def send_to_health_check(now, exit_status, descrip, aws_access_key_id, aws_secret_access_key, endpoint_url):
	dynamodb = boto3.client("dynamodb",
	aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name='us-east-1')
        
	dynamodb.put_item(
		TableName="HealthServices",
		Item={
			"id": {"S": "download_financial_data"},
			"identifier": {"S": f"{now}"},
			"ExitStatus": {"N": f"{exit_status}"},
			"Descrip": {"M": 
				{
					"Descrip": {
						"S": f"{descrip}"
					}
				}
			}
		}
	)
        		

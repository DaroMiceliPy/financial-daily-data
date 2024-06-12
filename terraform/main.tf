resource "aws_s3_bucket" "test-bucket" {
	bucket = "financial-data"
}

resource "aws_dynamodb_table" "HealthServices" {
	name = "HealthServices"
	billing_mode = "PAY_PER_REQUEST"
	hash_key = "id"
	
	attribute {
		name = "id"
		type = "S"
	}
	
	attribute {
		name = "identifier"
		type = "S"
	}
	
	global_secondary_index {
		name = "identifier-index"
		hash_key = "identifier"
		projection_type = "INCLUDE"
		non_key_attributes = ["ExitStatus", "Descrip"]
	}
}

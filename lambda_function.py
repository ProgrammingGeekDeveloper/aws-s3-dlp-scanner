import boto3
import re
import urllib.parse

s3 = boto3.client('s3')

# Configuration - Replace with your bucket name
QUARANTINE_BUCKET = 'scanner-quarantine-jail-denisgitonga'
# Regex to find AWS Access Key ID patterns
AWS_KEY_REGEX = r'AKIA[0-9A-Z]{16}' 

def lambda_handler(event, context):
    # Accessing the first record in the list [0]
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    file_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    try:
        # 1. Read the file content
        response = s3.get_object(Bucket=source_bucket, Key=file_key)
        content = response['Body'].read().decode('utf-8')
        
        # 2. Search for secrets
        if re.search(AWS_KEY_REGEX, content):
            print(f"SECURITY ALERT: AWS Secret Key detected in {file_key}!")
            
            # 3. Move file to Quarantine (Copy then Delete)
            new_key = f"quarantined-{file_key}"
            s3.copy_object(
                Bucket=QUARANTINE_BUCKET,
                CopySource={'Bucket': source_bucket, 'Key': file_key},
                Key=new_key
            )
            s3.delete_object(Bucket=source_bucket, Key=file_key)
            
            print(f"SUCCESS: {file_key} has been moved to {QUARANTINE_BUCKET}")
            return {"status": "QUARANTINED", "file": file_key}
            
        print(f"SCAN COMPLETE: No secrets found in {file_key}.")
        return {"status": "CLEAN", "file": file_key}

    except Exception as e:
        print(f"ERROR: Could not process file {file_key}. Reason: {str(e)}")
        raise e

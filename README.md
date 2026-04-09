# AWS S3 Leaked Secret Scanner (DLP)

## Project Overview
As a Security Professional, ensuring that sensitive data like AWS Access Keys are not accidentally uploaded to untrusted S3 buckets is critical. This project implements an automated **Data Loss Prevention (DLP)** workflow using a serverless architecture.

When a file is uploaded to a "Source" bucket, an S3 Event Notification triggers a Lambda function. The function scans the file content using Regex for AWS Access Key patterns. If a secret is found, the file is immediately moved to a private "Quarantine" bucket and deleted from the source.

## Architecture
- **Amazon S3**: Source and Quarantine storage.
- **AWS Lambda**: Python-based scanner logic.
- **Amazon EventBridge/S3 Events**: Event-driven trigger mechanism.
- **AWS IAM**: Execution role following the principle of **Least Privilege**.

## Key Features
- **Real-time Detection**: Scans happen within milliseconds of upload.
- **Automated Remediation**: No manual intervention required to secure leaked credentials.
- **Logging & Auditing**: Detailed execution logs stored in Amazon CloudWatch.

## Technical Implementation
- **Boto3**: Used for S3 object manipulation (Get, Copy, Delete).
- **Python Regex (`re`)**: Specifically targets the `AKIA` pattern for AWS Access Keys.
- **IAM Policy**: Custom JSON policy restricting access only to the specific buckets involved.

## How to Deploy
1. Create two S3 buckets: `source-bucket` and `quarantine-bucket`.
2. Create an IAM Role for Lambda with the permissions provided in `iam_policy.json`.
3. Deploy the `lambda_function.py` to an AWS Lambda function (Python 3.12).
4. Add an S3 Trigger to the Lambda for `s3:ObjectCreated:*` events on the source bucket.

## Future Enhancements
- Integration with **Amazon SES** to send email alerts to the SOC team.
- Adding support for more patterns (Secret Keys, Private Keys, PII).
- Implementation using **Infrastructure as Code (Terraform)**.

  ## Security Implementation Details
  **Principle of Least Privilege**: The execution role is scoped strictly to the source and quarantine buckets. It has no access to other AWS resources.
  **Attack Surface Reduction**: By using a serverless architecture (Lambda), we eliminate the need to manage and patch underlying EC2 instances.
 **Automated Remediation**: The "mean time to respond" (MTTR) is reduced to seconds, as the system acts immediately upon file upload without human intervention.


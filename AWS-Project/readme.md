# US EV Data – AWS ETL Project

An automated, serverless, event-driven data pipeline on AWS (Tokyo region) to ingest, transform, and store U.S. electric vehicle registration data for analysis and insights.

---

## 📘 Project Description

This project analyzes the population of electric vehicles (EVs) across the United States using open data from Washington State’s Open Data portal. The dataset includes:

- VIN  
- Vehicle make and model  
- Model year  
- Electric range  
- Vehicle type  
- Registration location (state, county, city)  

The goal is to build a fully automated AWS pipeline that ingests this data, applies transformations, and loads it into a PostgreSQL database for downstream analysis by data analysts, policymakers, and EV enthusiasts.

---

## 🏗️ Architecture Overview

A fully serverless, event-driven architecture deployed inside a VPC for security. The workflow is triggered on a schedule, pulls data from a public API, persists raw files in S3, and loads cleaned records into Amazon RDS (PostgreSQL).

---

## 🔧 Key AWS Components

| AWS Service                | Purpose                                                                       |
|----------------------------|-------------------------------------------------------------------------------|
| AWS Secrets Manager        | Stores S3 bucket name and PostgreSQL credentials                              |
| Amazon EventBridge         | Schedules and triggers the pipeline, injecting secrets                        |
| AWS Step Functions         | Orchestrates the ETL workflow steps                                           |
| AWS Lambda                 |  
  - Extraction: fetches EV data from API, writes raw JSON/CSV to S3  
  - Loading: reads S3 objects and inserts into PostgreSQL with conflict handling |
| Amazon SNS                 | Sends success/failure notifications                                            |
| Amazon RDS (PostgreSQL)    | Stores cleaned, structured EV registration data                                |
| Amazon S3                  | Temporary storage for raw JSON/CSV files                                       |
| Amazon CloudWatch          | Logs and monitors Lambda functions, Step Functions, and overall pipeline       |
| VPC + Interface Endpoints  | Secure, private communication to Secrets Manager and S3 without internet egress|

---

## 🔁 Workflow Summary

1. **Scheduling & Triggering**  
   Amazon EventBridge fires on a defined schedule and invokes the Step Functions state machine, passing in secrets from AWS Secrets Manager.

2. **Extraction Phase**  
   - A Lambda function calls the public EV API.  
   - Raw data is written to an S3 bucket.  
   - SNS publishes success or error notifications.

3. **Loading Phase**  
   - A second Lambda function reads the S3 file.  
   - Records are transformed and upserted into the RDS PostgreSQL instance.  
   - A final SNS notification confirms pipeline completion or failure.

---

## 🔒 Security

- All components run inside a dedicated VPC.  
- Security groups restrict access to RDS and Lambda functions.  
- VPC interface endpoints enable private, secure calls to AWS Secrets Manager and S3.  
- Credentials never leave Secrets Manager; Lambda retrieves them at runtime.

---

## 📊 Architecture Diagram

Replace the image path below with your repository’s actual diagram location.

```markdown
![AWS Architecture](./AWS_Architecture.png)

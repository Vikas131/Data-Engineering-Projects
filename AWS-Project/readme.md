# 🚗 US EV Data – AWS ETL Project

## 📘 Project Description

This project focuses on analyzing the population of electric vehicles (EVs) across the United States using publicly available data from Washington State’s Open Data portal. The dataset includes details such as VIN, vehicle make and model, model year, electric range, vehicle type, and registration location (state, county, city).

The goal of the project is to build an automated AWS data pipeline that ingests, transforms, and stores this dataset for further analysis, providing insights to data analysts, policymakers, and EV enthusiasts.

---

## 🏗️ Architecture Overview

This project leverages a fully serverless, event-driven architecture within a secure VPC on AWS (Tokyo region) to automate the ingestion and analysis of U.S. electric vehicle data.

---

## 🔧 Key AWS Components

| AWS Service               | Purpose                                                                               |
|---------------------------|---------------------------------------------------------------------------------------|
| AWS Secrets Manager       | Stores S3 bucket name and PostgreSQL credentials                                      |
| Amazon EventBridge        | Triggers the pipeline on schedule and injects secrets                                 |
| AWS Step Functions        | Orchestrates the entire ETL process                                                   |
| AWS Lambda                | Extracts data from API and loads it into PostgreSQL                                   |
| Amazon SNS                | Sends success/failure notifications                                                   |
| Amazon RDS (PostgreSQL)   | Stores cleaned and structured EV data                                                 |
| Amazon S3                 | Temporary storage for raw JSON/CSV files                                              |
| Amazon CloudWatch         | Logs for Lambda, Step Functions, and monitoring                                       |
| VPC + Endpoints           | Ensures secure communication within the AWS environment                               |

---

## 🔁 Workflow Summary

1. Scheduling & Triggering

   EventBridge triggers the Step Function, passing secrets from Secrets Manager.

2. Extraction Phase

   Lambda fetches EV data from the public API and stores it in S3. SNS sends a notification on success or failure.

3. Loading Phase

   Another Lambda reads the S3 file and loads data into the RDS PostgreSQL instance. A final SNS alert confirms success or failure.

4. Security

   All services are deployed inside a VPC with appropriate security groups and private endpoints for Secrets Manager and S3.

---

## 🔒 Security

All services are deployed inside a VPC with appropriate security groups and private endpoints for Secrets Manager and S3.

---

## 📊 Architecture Diagram

📎 Replace the image file path below with your final diagram location in your repo.

---

## 🧰 Tech Stack

This project was implemented using a combination of Python-based data processing and AWS serverless components to construct an end-to-end ETL pipeline for electric vehicle data ingestion and analysis.

### Programming Language

- Python 3.12

### Python Libraries

- requests – For HTTP GET requests to the public API  
- pandas – Data manipulation and transformation  
- boto3 – AWS SDK for Python, used for interacting with S3 and Secrets Manager  
- sqlalchemy – For constructing and managing the PostgreSQL connection string  
- psycopg2 – PostgreSQL database driver used for executing queries  
- json, io, os, logging, datetime, unittest – Standard libraries for auxiliary tasks such as logging, environment variable handling, and in-memory stream management  

### AWS Services

| AWS Service                         | Purpose                                                                                             |
|-------------------------------------|-----------------------------------------------------------------------------------------------------|
| AWS Lambda                          | Serverless compute functions for data extraction and loading                                       |
| Amazon S3                           | Temporary staging area for raw data in CSV/JSON format                                             |
| Amazon RDS (PostgreSQL 13.20)       | Persistent relational database for structured EV data                                               |
| AWS Secrets Manager                 | Secure storage for database credentials and S3 bucket name                                          |
| AWS Step Functions                  | Workflow orchestration to manage the ETL process                                                    |
| Amazon EventBridge                  | Scheduled trigger to initiate the workflow                                                          |
| Amazon SNS                          | Notification service for success/failure alerts                                                     |
| Amazon CloudWatch                   | Monitoring and log aggregation for all execution components                                         |
| VPC, Security Groups, and Endpoints | Used to isolate and secure service interactions within a private network                            |

### Deployment

- Manual Configuration – All AWS resources were provisioned and configured manually via the AWS Management Console; no infrastructure-as-code tools (e.g., Terraform, CloudFormation, or CDK) were used.

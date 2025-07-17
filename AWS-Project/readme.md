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

```markdown
![AWS Architecture](AWS-Project/Flowcharts/AWS_Architecture.png)

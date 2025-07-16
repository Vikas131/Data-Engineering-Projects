import requests
import io
import boto3
import pandas as pd
from datetime import date
import os,logging


def lambda_handler(event, context):
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    bucket_name = event["s3-bucket-name"]
    url = "https://data.wa.gov/api/views/f6w7-q2d2/rows.json?accessType=DOWNLOAD"

    # Send a GET request
    response = requests.get(url)

    # Check the response
    if response.ok:
        raw_json_data = response.json()
        raw_column_data= raw_json_data["meta"]["view"]["columns"]  # Print or process the JSON data
        column_names = []
        for items in raw_column_data:
            if(items["id"]!=-1):
                column_names.append(items["name"])
                # print(raw_json_data["data"][0])

        raw_data = []
        for i in range(0,300):
            raw_data.append(raw_json_data["data"][i])
        # print(raw_data)

        formatted_data = {}
        for i, name in enumerate(column_names):
            # print(i,name)
            formatted_data[name] = []
            for row in raw_data:
                formatted_data[name].append(row[i+8])
                # print(formatted_data)
    
        df = pd.DataFrame(formatted_data)
        # # print(df)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        logger.info("Converted to csv successfully")

        s3 = boto3.client("s3")
        # bucket_name = event["bucket_name"]
        file_name = f"raw_data/date={date.today().strftime('%Y%m%d')}/raw_data.csv"
        logger.info(f"File name:{file_name}")

        try:
            s3.put_object(Bucket=bucket_name, Key=file_name, Body=csv_buffer.getvalue())
            logger.info(f"CSV successfully saved to s3://{bucket_name}/{file_name}")
            return {
                'status': "success",
                's3_path': f"s3://{bucket_name}/{file_name}",
                'bucket_name':bucket_name,
                'file_name':file_name
            }
        except Exception as e:
            logger.error(f"Error saving CSV to S3: {e}")
            raise e
 
    else:
        raise Exception(f"Data fetch failed with status code {response.status_code}")


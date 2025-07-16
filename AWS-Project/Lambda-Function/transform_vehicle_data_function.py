import boto3, logging
import pandas as pd
from io import StringIO
from datetime import datetime
from sqlalchemy import create_engine, text
import psycopg2
from unittest import result
import json

def lambda_handler(event, context):

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # s3_file_path = event['s3_path']
    bucket_name = event['bucket_name']
    file_name = event['file_name']
    # bucket_name = "electricvehicleus"
    # file_name = "raw_data/date=20250710/raw_data.csv"
    # logger.info(f'S3 file path: {s3_file_path}')
    logger.info(f'Bucket name:{bucket_name}')
    logger.info(f'File name: {file_name}')

    # read csv file from S3
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    body = response['Body'].read().decode('utf-8')

    df = pd.read_csv(StringIO(body))
    # logger.info(df.head())

    df.drop(columns=['Clean Alternative Fuel Vehicle (CAFV) Eligibility','Base MSRP',
    'DOL Vehicle ID', 'Vehicle Location', 'Legislative District','WAOFM - GIS - Legislative District Boundary',
     'Electric Utility', '2020 Census Tract','Counties','Congressional Districts'], inplace=True)

    df.rename(columns=
    {'VIN (1-10)': 'vin_code',
    'County':'county',
    'City':'city',
    'State':'state',
    'Postal Code':'postal_code',
    'Model Year':'model_year',
    'Make':'make',
    'Model':'model_name',
    'Electric Vehicle Type':'vehicle_type',
    'Electric Range':'electric_range'}, inplace=True)

    # logger.info(df.columns)

    df['loaddate'] = datetime.today()
    logger.info(df.head())

    secrets = get_secrets('rds/postgres')
    # connect to postgresql database
    username = secrets['username']
    password = secrets['password']
    port = secrets['port']
    db_name = secrets['db_name']
    table_name = 'electric_vehicle_us'
    host = secrets['host']

    postgres_url = f'postgresql+psycopg://{username}:{password}@{host}:{port}/{db_name}'
    logger.info(f'Postgres url: {postgres_url}')
    engine = create_engine(postgres_url)

    # Convert to dicts for parameter binding
    records = df.to_dict(orient="records")

    # Define SQL with ON CONFLICT clause
    sql = text("""
        INSERT INTO electric_vehicle_us (
            vin_code, county, city, state, postal_code, model_year, make, model_name,
            vehicle_type, electric_range, loaddate
        )
        VALUES (
            :vin_code, :county, :city, :state, :postal_code, :model_year, :make, :model_name,
            :vehicle_type, :electric_range, :loaddate
        )
        ON CONFLICT (vin_code, postal_code, loaddate) DO NOTHING
    """)

    inserted_records = 0
    with engine.begin() as conn:
        # df.to_sql(table_name, conn, if_exists='append', index=False)
        for record in records:
            result = conn.execute(sql, record)
            if result.rowcount == 1:
                inserted_records += 1
        
        skipped_records = len(records) - inserted_records
        logger.info(f'Inserted records: {inserted_records}')
        logger.info(f'Skipped records: {skipped_records}')

    # TODO implement
    return {
        'statusCode': "success",
    }

def get_secrets(secret_name):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    logger.info('Trying to fetch secret creds')
    secrets_client = boto3.client('secretsmanager')
    response = secrets_client.get_secret_value(SecretId=secret_name)
    secret = response['SecretString']
    logger.info('Secrets fetched successfully')
    return json.loads(secret)

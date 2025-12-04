# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

import boto3
import os
import json
import logging
import uuid

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_client = boto3.client("dynamodb")


def handler(event, context):
    request_id = context.request_id
    table = os.environ.get("TABLE_NAME")
    
    logger.info(json.dumps({
        "message": "Processing request",
        "request_id": request_id,
        "table_name": table,
        "event_type": "api_request"
    }))
    
    if event["body"]:
        item = json.loads(event["body"])
        logger.info(json.dumps({
            "message": "Received payload",
            "request_id": request_id,
            "payload": item,
            "event_type": "payload_received"
        }))
        year = str(item["year"])
        title = str(item["title"])
        id = str(item["id"])
        dynamodb_client.put_item(
            TableName=table,
            Item={"year": {"N": year}, "title": {"S": title}, "id": {"S": id}},
        )
        logger.info(json.dumps({
            "message": "Successfully inserted data",
            "request_id": request_id,
            "item_id": id,
            "event_type": "data_inserted"
        }))
        message = "Successfully inserted data!"
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": message}),
        }
    else:
        logger.info(json.dumps({
            "message": "Received request without payload",
            "request_id": request_id,
            "event_type": "no_payload"
        }))
        default_id = str(uuid.uuid4())
        dynamodb_client.put_item(
            TableName=table,
            Item={
                "year": {"N": "2012"},
                "title": {"S": "The Amazing Spider-Man 2"},
                "id": {"S": default_id},
            },
        )
        logger.info(json.dumps({
            "message": "Successfully inserted default data",
            "request_id": request_id,
            "item_id": default_id,
            "event_type": "data_inserted"
        }))
        message = "Successfully inserted data!"
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": message}),
        }

import logging
import os

import boto3
from aws_lambda_powertools import Logger
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

boto3.set_stream_logger()
boto3.set_stream_logger("botocore")
logger = Logger(service="wordle")

if os.getenv("DYNAMODB_GAME_TABLE") is not None:
    WORDLE_DYNAMODB_TABLE: str = os.getenv("DYNAMODB_GAME_TABLE")
else:
    WORDLE_DYNAMODB_TABLE: str = "Wordle"

if os.getenv("DYNAMODB_ENDPOINT_URL") is not None:
    DYNAMO_ENDPOINT_URL: str = os.getenv("DYNAMODB_ENDPOINT_URL")
else:
    DYNAMO_ENDPOINT_URL: str = "http://localhost:8000"

if os.getenv("AWS_REGION") is not None:
    AWS_REGION: str = os.getenv("AWS_REGION")
else:
    AWS_REGION: str = "us-east-1"

dynamodb = boto3.resource("dynamodb")


def get_wordle_game(user_id):
    table = dynamodb.Table(WORDLE_DYNAMODB_TABLE)
    response = table.query(KeyConditionExpression=Key("user_id").eq(user_id))
    if len(response["Items"]) > 0:
        return response["Items"][0]
    else:
        return None


def put_wordle_game(user_id, game):
    table = dynamodb.Table(WORDLE_DYNAMODB_TABLE)
    try:
        response = table.put_item(Item={"user_id": user_id, "game": game.to_json()})
        return response
    except ClientError as e:
        logger.error(e.response["Error"]["Message"])
        return None


with open("words.txt", "r") as f:
    WORDLEBANK = [word.strip().upper() for word in f.readlines()]

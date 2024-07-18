import os
import urllib3
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum


app = FastAPI()


class Message(BaseModel):
    message: str


def get_aws_secret():
    http = urllib3.PoolManager()
    headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get('AWS_SESSION_TOKEN')}
    secrets_extension_http_port = "2773"
    secrets_extension_endpoint = "http://localhost:" + \
                                 secrets_extension_http_port + \
                                 "/secretsmanager/get?secretId=" + \
                                 "MongoDBSecret-dev"

    resp = http.request(
        "GET",
        secrets_extension_endpoint,
        headers=headers
    )
    print('Secret data:', resp.data)
    secret = json.loads(resp.data)
    secretValue = json.loads(secret['SecretString'])
    return secretValue

@app.post("/asset-management/v1/metadata-generation")
async def metadata_generation(body: Message):
    if body.message == "OK":
        return {"statusCode": 200}
    else:
        raise HTTPException(status_code=400, detail="Invalid request")


@app.get("/asset-management/v1/metadata/feedback")
async def get_feedback():
    # mongo_db_secret = get_aws_secret()
    return {"message": "Feedback retrieved successfully"}


@app.post("/asset-management/v1/metadata-generation")
async def metadata_generation(body: Message):
    if body.message == "OK":
        return {"statusCode": 200}
    else:
        raise HTTPException(status_code=400, detail="Invalid request")


@app.post("/asset-management/v1/metadata/feedback")
async def post_feedback(body: Message):
    if body.message == "OK":
        return {"statusCode": 200}
    else:
        raise HTTPException(status_code=400, detail="Invalid request")


@app.put("/asset-management/v1/metadata/feedback")
async def put_feedback(body: Message):
    if body.message == "OK":
        return {"statusCode": 200}
    else:
        raise HTTPException(status_code=400, detail="Invalid request")


@app.get("/health")
async def health_check():
    return {"status": "OK"}

handler = Mangum(app)

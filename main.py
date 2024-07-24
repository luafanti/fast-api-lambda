import boto3
import json
import base64
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum

app = FastAPI()

bedrock = boto3.client(service_name='bedrock-runtime',region_name='eu-central-1')

modelId = 'amazon.titan-text-lite-v1'
accept = 'application/json'
contentType = 'application/json'

class Message(BaseModel):
    message: str


def get_aws_secret():
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="eu-central-1"
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId='MongoDBSecret-dev'
        )
    except Exception as e:
        print("Error occurred while retrieving the secret: ", e)
        return None

    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = base64.b64decode(get_secret_value_response['SecretBinary'])

    secretValue = json.loads(secret)
    return secretValue

@app.post("/asset-management/v1/metadata-generation")
async def metadata_generation(body: Message):
    if body.message == "OK":
        return {"statusCode": 200}
    else:
        raise HTTPException(status_code=400, detail="Invalid request")


@app.post("/asset-management/v1/metadata-generation")
async def metadata_generation(body: Message):
    if body.message == "OK":
        return {"statusCode": 200}
    else:
        raise HTTPException(status_code=400, detail="Invalid request")

@app.get("/asset-management/v1/metadata/feedback")
async def get_feedback():
    secret = get_aws_secret()
    return {"message": "Feedback retrieved successfully", "secret": secret}


@app.post("/asset-management/v1/metadata/feedback")
async def post_feedback(body: Message):

    request_message = body.message
    body = json.dumps({
        "inputText": request_message,
        "textGenerationConfig": {
            "maxTokenCount": 3072,
            "stopSequences": [],
            "temperature": 0.7,
            "topP": 0.9
        }
    })

    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    print(json.dumps(response_body))
    result = response_body.get('results')[0].get('outputText')
    return {"modelResponse": result}


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

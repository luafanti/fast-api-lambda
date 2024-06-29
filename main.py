from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum

app = FastAPI()


class Message(BaseModel):
    message: str


@app.post("/asset-management/v1/metadata-generation")
async def metadata_generation(body: Message):
    if body.message == "OK":
        return {"statusCode": 200}
    else:
        raise HTTPException(status_code=400, detail="Invalid request")


@app.get("/asset-management/v1/metadata/feedback")
async def get_feedback():
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

handler = Mangum(app)

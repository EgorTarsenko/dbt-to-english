from fastapi import FastAPI, File, UploadFile, Form
from typing import Annotated
from tr_dbt_to_english import DbtToEnglish
from fastapi.responses import StreamingResponse
import json


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.post("/get_node_in_english")
async def get_node_in_english(catalog_file: Annotated[UploadFile, File()],
                              manifest_file: Annotated[UploadFile, File()],
                              node_to_parse: Annotated[str, Form()],
                              prompt: Annotated[str, Form()]):
    manifest_str = await manifest_file.read()
    catalog_str = await catalog_file.read()
    manifest = json.loads(manifest_str)
    catalog = json.loads(catalog_str)
    return StreamingResponse(DbtToEnglish.upload_dbt_node(
        node_to_parse,
        manifest,
        catalog,
        prompt
    ), media_type='text/plain')

from fastapi import FastAPI
from src.services.github_service import fetch_repository_bundle
from src.services.summarizer import summarize_repository
from src.auxiliary import utils
from src.auxiliary.config import LLM_PROVIDER
from src.llm.openai_provider import OpenAIProvider
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from requests import Request
import json
import re
from typing import Union

if LLM_PROVIDER == "openai":
    llm = OpenAIProvider()
else:
    raise Exception(
        f"Currently only OpenAI LLM is supported, while {LLM_PROVIDER} was requested"
    )

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"status": "error", "message": "Invalid request format"},
    )


@app.post(
    "/summarize", response_model=Union[utils.SummarizeSuccess, utils.SummarizeError]
)
async def summarize(request: utils.SummarizeRequest):
    try:
        repo_url = str(request.github_url)

        bundle = await fetch_repository_bundle(repo_url)

        utils.logger.info(f"bundle keys: {bundle.keys()}")

        result = await summarize_repository(bundle=bundle, llm=llm)

        utils.logger.info(type(result))
        utils.logger.info(f"result: {result} ### End")

        raw_output = result
        try:
            cleaned = re.sub(r"```json|```", "", result).strip()
            result = json.loads(cleaned)
        except json.JSONDecodeError as e:
            return utils.SummarizeError(
                message=f"LLM returned invalid JSON: {e}\nRaw output:\n{raw_output}"
            )

        return utils.SummarizeSuccess(**result)

    except Exception as e:
        return utils.SummarizeError(message=str(e))

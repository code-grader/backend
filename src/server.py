from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import logging

import asyncio
import json

from .utils.http_response import create_response
from .lib.analyze_code import analyze_code
from .lib.code_suggestion import generate_suggestion

app = FastAPI()


class CodeSnippet(BaseModel):
    code: str


@app.get("/")
async def read_root():
    return create_response(message="Server is running!")


@app.websocket("/ws/code")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message["type"] == "code_submit":
                code_snippet = CodeSnippet(code=message["code"])

                # Create tasks for analysis and suggestions
                analysis_task = asyncio.create_task(analyze_code(code_snippet.code))
                suggestion_task = asyncio.create_task(
                    generate_suggestion(code_snippet.code)
                )

                # Gather and handle results concurrently
                done, pending = await asyncio.wait(
                    {analysis_task, suggestion_task},
                    return_when=asyncio.FIRST_COMPLETED,
                )

                for task in done:
                    if task == analysis_task:
                        analysis_result = task.result()
                        await websocket.send_json(
                            {
                                "type": "analysis_result",
                                "data": analysis_result,
                            }
                        )
                    elif task == suggestion_task:
                        code_suggestion = task.result()
                        for line in code_suggestion.split("\n"):
                            await websocket.send_json(
                                {
                                    "type": "code_suggestion",
                                    "data": line,
                                }
                            )
                            await asyncio.sleep(0.1)

                # Ensure to send out the remaining task's result
                for task in pending:
                    result = await task
                    if task == analysis_task:
                        await websocket.send_json(
                            {
                                "type": "analysis_result",
                                "data": result,
                            }
                        )
                    elif task == suggestion_task:
                        for line in result.split("\n"):
                            await websocket.send_json(
                                {
                                    "type": "code_suggestion",
                                    "data": line,
                                }
                            )
                            await asyncio.sleep(0.1)

    except WebSocketDisconnect:
        logging.info("Client disconnected")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

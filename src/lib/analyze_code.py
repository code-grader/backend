from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Any, Dict

from .llm_model import llm_model


class CodeRating(BaseModel):
    readability: str = Field(
        title="Code Readability",
        description="The rating of the code's readability out of 10, higher is better",
    )
    optimisation: str = Field(
        title="Code Optimisation",
        description="The rating of the code's optimisation out of 10, higher is better",
    )
    complexity: str = Field(
        title="Code Complexity",
        description="The rating of the code's complexity out of 10, lower is better",
    )


async def analyze_code(code: str) -> Dict[str, Any]:
    parser = PydanticOutputParser(pydantic_object=CodeRating)
    format_instructions = parser.get_format_instructions()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Rate the following code on a scale of 1 to 10 based on readability, optimisation, and complexity.",
            ),
            ("user", "{input_code}"),
            ("system", "{format_instructions}"),
        ],
    )

    chain = prompt | llm_model

    response = chain.invoke(
        {"input_code": code, "format_instructions": format_instructions}
    )

    return response

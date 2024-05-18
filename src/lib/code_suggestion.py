from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from .llm_model import llm_model


class CodeBlock(BaseModel):
    code: str = Field(title="Code", description="The optimised code function")
    language: str = Field(
        title="Language", description="The programming language of the code"
    )


async def generate_suggestion(code: str) -> str:
    # use pydantic output parser
    parser = PydanticOutputParser(pydantic_object=CodeBlock)
    format_instructions = parser.get_format_instructions()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Optimize the following code for readability, complexity and performance.",
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

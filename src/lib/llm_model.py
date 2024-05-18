from src.utils.environment import env
from langchain_community.llms import Ollama

llm_model = Ollama(
    model=env["MODEL_NAME"], base_url=env["OLLAMA_API"], format="json", temperature=0
)

TEST_CODE = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
"""

"""
from langchain.output_parsers import PydanticOutputParser
prompt = ChatPromptTemplate.from_messages(messages)
    parser = PydanticOutputParser(pydantic_object=schemas.FollowUpQuestions)

    prompt.partial_variables = {"format_instructions": parser.get_format_instructions()} prompt = ChatPromptTemplate.from_messages(messages)
    parser = PydanticOutputParser(pydantic_object=schemas.FollowUpQuestions)

    prompt.partial_variables = {"format_instructions": parser.get_format_instructions()}
"""

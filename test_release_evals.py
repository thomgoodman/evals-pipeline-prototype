from app import assistant_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import pytest
import sys


def create_eval_chain(
    agent_response,
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
    output_parser=StrOutputParser(),
):
    delimiter = "####"
    eval_system_prompt = f"""You are an assistant that evaluates whether or not an assistant is producing valid quizzes.
  The assistant should be producing output in the format of Question N:{delimiter} <question N>?"""

    eval_user_message = f"""You are evaluating a generated quiz based on the context that the assistant uses to create the quiz.
  Here is the data:
    [BEGIN DATA]
    ************
    [Response]: {agent_response}
    ************
    [END DATA]

Read the response carefully and determine if it looks like a quiz or test. Do not evaluate if the information is correct
only evaluate if the data is in the expected format.

Output Y if the response is a quiz, output N if the response does not look like a quiz.
"""
    eval_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", eval_system_prompt),
            ("human", eval_user_message),
        ]
    )

    return eval_prompt | llm | output_parser


@pytest.fixture
def known_bad_result():
    return "There are lots of interesting facts. Tell me more about what you'd like to know"


@pytest.fixture
def quiz_request():
    return "Give me a quiz about Geography"


def test_model_graded_eval(quiz_request, setup_logging, langchain_tracer):
    logger = setup_logging
    logger.info("Starting model graded eval test")

    assistant = assistant_chain()
    logger.info(f"Sending request: {quiz_request}")

    result = assistant.invoke(
        {"question": quiz_request}, config={"callbacks": [langchain_tracer]}
    )
    logger.info(f"Assistant response: {result}")

    logger.info("Creating evaluation chain")
    eval_agent = create_eval_chain(result)

    logger.info("Invoking evaluation agent")
    eval_response = eval_agent.invoke({}, config={"callbacks": [langchain_tracer]})
    logger.info(f"Evaluation response: {eval_response}")

    assert eval_response == "Y"


def test_model_graded_eval_should_fail(
    known_bad_result, setup_logging, langchain_tracer
):
    logger = setup_logging
    logger.info("Starting model graded eval failure test")
    logger.info(f"Using known bad result: {known_bad_result}")

    logger.info("Creating evaluation chain")
    eval_agent = create_eval_chain(known_bad_result)

    logger.info("Invoking evaluation agent")
    eval_response = eval_agent.invoke({}, config={"callbacks": [langchain_tracer]})
    logger.info(f"Evaluation response: {eval_response}")

    assert (
        eval_response == "N"
    ), f"Expected the response to be 'N' for a non-quiz input, \
    got '{eval_response}'"


# Run all tests if script is executed directly
if __name__ == "__main__":
    print("Running all tests with pytest...\n")
    import pytest

    # Run all tests in this file
    pytest.main(["-v", __file__])

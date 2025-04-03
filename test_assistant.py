from app import assistant_chain
import os
import sys
import pytest

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


def test_science_quiz(setup_logging, langchain_tracer):
    logger = setup_logging
    logger.info("Testing science quiz generation")

    assistant = assistant_chain()
    question = "Generate a quiz about science."
    logger.info(f"Sending request: {question}")

    answer = assistant.invoke(
        {"question": question}, config={"callbacks": [langchain_tracer]}
    )
    logger.info(f"Response received: {answer}")

    expected_subjects = ["davinci", "telescope", "physics", "curie"]
    logger.info(f"Checking for expected subjects: {expected_subjects}")

    assert any(
        subject.lower() in answer.lower() for subject in expected_subjects
    ), f"Expected the assistant questions to include '{expected_subjects}', but it did not"


def test_geography_quiz(setup_logging, langchain_tracer):
    logger = setup_logging
    logger.info("Testing geography quiz generation")

    assistant = assistant_chain()
    question = "Generate a quiz about geography."
    logger.info(f"Sending request: {question}")

    answer = assistant.invoke(
        {"question": question}, config={"callbacks": [langchain_tracer]}
    )
    logger.info(f"Response received: {answer}")

    expected_subjects = ["paris", "france", "louvre"]
    logger.info(f"Checking for expected subjects: {expected_subjects}")

    assert any(
        subject.lower() in answer.lower() for subject in expected_subjects
    ), f"Expected the assistant questions to include '{expected_subjects}', but it did not"


def test_decline_unknown_subjects(setup_logging, langchain_tracer):
    logger = setup_logging
    logger.info("Testing decline for unknown subjects")

    assistant = assistant_chain()
    question = "Generate a quiz about Rome"
    logger.info(f"Sending request: {question}")

    answer = assistant.invoke(
        {"question": question}, config={"callbacks": [langchain_tracer]}
    )
    logger.info(f"Response received: {answer}")

    # We'll look for a substring of the message the bot prints when it gets a question about any
    decline_response = "I'm sorry"
    logger.info(f"Checking for decline response: '{decline_response}'")

    assert (
        decline_response.lower() in answer.lower()
    ), f"Expected the bot to decline with '{decline_response}' got {answer}"


# Run all tests if script is executed directly
if __name__ == "__main__":
    print("Running all tests with pytest...\n")
    # Run all tests in this file
    pytest.main(["-v", __file__])

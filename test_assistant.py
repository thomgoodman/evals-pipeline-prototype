from app import assistant_chain
from app import system_message
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

import os
import openai
import sys
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# Ensure OpenAI API key is set
if "OPENAI_API_KEY" not in os.environ:
    raise ValueError(
        "OPENAI_API_KEY environment variable is not set. Please set it before running tests."
    )

# Set API key for OpenAI module directly
openai.api_key = os.environ["OPENAI_API_KEY"]


def eval_expected_words(
    system_message,
    question,
    expected_words,
    human_template="{question}",
    llm=ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.environ["OPENAI_API_KEY"],
    ),
    output_parser=StrOutputParser(),
):
    print(f"\n\n=== Testing with question: '{question}' ===")
    print(f"Looking for words: {expected_words}")

    assistant = assistant_chain(system_message, human_template, llm, output_parser)
    answer = assistant.invoke({"question": question})

    print("\n--- LLM RESPONSE ---")
    print(answer)
    print("-------------------\n")

    # Check if any expected word is in the answer
    found_words = [word for word in expected_words if word.lower() in answer.lower()]
    not_found_words = [
        word for word in expected_words if word.lower() not in answer.lower()
    ]

    print(f"Words found: {found_words if found_words else 'None'}")
    print(f"Words missing: {not_found_words if not_found_words else 'None'}")

    # Check if the response contains a quiz with questions
    contains_questions = "Question" in answer and not "I'm sorry" in answer
    print(f"Contains quiz questions: {'Yes' if contains_questions else 'No'}")

    assert any(
        word.lower() in answer.lower() for word in expected_words
    ), f"Expected the assistant questions to include one of \
    '{expected_words}', but none were found"

    assert (
        contains_questions
    ), "Expected the response to contain quiz questions, but it appears to be a refusal."

    print("Test PASSED!\n")
    return answer


def evaluate_refusal(
    system_message,
    question,
    decline_response,
    human_template="{question}",
    llm=ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.environ["OPENAI_API_KEY"],
    ),
    output_parser=StrOutputParser(),
):
    print(f"\n\n=== Testing refusal with question: '{question}' ===")
    print(f"Looking for decline response: '{decline_response}'")

    assistant = assistant_chain(system_message, human_template, llm, output_parser)

    answer = assistant.invoke({"question": question})

    print("\n--- LLM RESPONSE ---")
    print(answer)
    print("-------------------\n")

    contains_decline = decline_response.lower() in answer.lower()
    print(f"Contains decline response: {'Yes' if contains_decline else 'No'}")

    assert (
        decline_response.lower() in answer.lower()
    ), f"Expected the bot to decline with \
    '{decline_response}' got {answer}"

    print("Test PASSED!\n")
    return answer


"""
  Test cases
"""


def test_science_quiz():
    question = "Generate a quiz about science."
    expected_subjects = ["davinci", "telescope", "physics", "curie"]
    return eval_expected_words(system_message, question, expected_subjects)


def test_geography_quiz():
    question = "Generate a quiz about geography."
    expected_subjects = ["paris", "france", "louvre"]
    return eval_expected_words(system_message, question, expected_subjects)


def test_refusal_rome():
    question = "Help me create a quiz about Rome"
    decline_response = "I'm sorry"
    return evaluate_refusal(system_message, question, decline_response)


# Run all tests if script is executed directly
if __name__ == "__main__":
    print("Running all tests...\n")

    try:
        print("\n\n========== RUNNING SCIENCE QUIZ TEST ==========")
        science_result = test_science_quiz()

        print("\n\n========== RUNNING GEOGRAPHY QUIZ TEST ==========")
        geography_result = test_geography_quiz()

        print("\n\n========== RUNNING REFUSAL TEST ==========")
        refusal_result = test_refusal_rome()

        print("\n\nAll tests passed successfully!")

    except AssertionError as e:
        print(f"\n\nTEST FAILED: {e}", file=sys.stderr)
        sys.exit(1)

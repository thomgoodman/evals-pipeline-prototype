from app import assistant_chain
import os
import sys

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


def test_science_quiz():
    assistant = assistant_chain()
    question = "Generate a quiz about science."
    answer = assistant.invoke({"question": question})
    expected_subjects = ["davinci", "telescope", "physics", "curie"]
    print(answer)
    assert any(
        subject.lower() in answer.lower() for subject in expected_subjects
    ), f"Expected the assistant questions to include '{expected_subjects}', but it did not"


def test_geography_quiz():
    assistant = assistant_chain()
    question = "Generate a quiz about geography."
    answer = assistant.invoke({"question": question})
    expected_subjects = ["paris", "france", "louvre"]
    print(answer)
    assert any(
        subject.lower() in answer.lower() for subject in expected_subjects
    ), f"Expected the assistant questions to include '{expected_subjects}', but it did not"


def test_decline_unknown_subjects():
    assistant = assistant_chain()
    question = "Generate a quiz about Rome"
    answer = assistant.invoke({"question": question})
    print(answer)
    # We'll look for a substring of the message the bot prints when it gets a question about any
    decline_response = "I'm sorry"
    assert (
        decline_response.lower() in answer.lower()
    ), f"Expected the bot to decline with '{decline_response}' got {answer}"


# Run all tests if script is executed directly
if __name__ == "__main__":
    print("Running all tests...\n")

    try:
        print("\n\n========== RUNNING SCIENCE QUIZ TEST ==========")
        science_result = test_science_quiz()

        print("\n\n========== RUNNING GEOGRAPHY QUIZ TEST ==========")
        geography_result = test_geography_quiz()

        print("\n\n========== RUNNING REFUSAL TEST ==========")
        refusal_result = test_decline_unknown_subjects()

        print("\n\nAll tests passed successfully!")

    except AssertionError as e:
        print(f"\n\nTEST FAILED: {e}", file=sys.stderr)
        sys.exit(1)

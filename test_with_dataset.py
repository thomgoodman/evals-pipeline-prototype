from app import assistant_chain
import pytest

# In a real application you would load your dataset from a file or logging tool.
# Here we have a mix of examples with slightly different phrasing that our quiz application can support
# and things we don't support.
dataset = [
    {
        "input": "I'm trying to learn about science, can you give me a quiz to test my knowledge",
        "response": "science",
        "subjects": ["davinci", "telescope", "physics", "curie"],
    },
    {
        "input": "I'm an geography expert, give a quiz to prove it?",
        "response": "geography",
        "subjects": ["paris", "france", "louvre"],
    },
    {
        "input": "Quiz me about Italy",
        "response": "geography",
        "subjects": ["rome", "alps", "sicily"],
    },
]


def test_on_dataset(setup_logging, langchain_tracer):
    logger = setup_logging
    logger.info("Starting dataset-based testing")

    assistant = assistant_chain()
    for idx, row in enumerate(dataset):
        user_input = row["input"]
        expected_category = row["response"]
        expected_subjects = row.get("subjects", None)

        logger.info(f"Testing example {idx+1}/{len(dataset)}: {user_input}")
        logger.info(f"Expected category: {expected_category}")
        logger.info(f"Expected subjects: {expected_subjects}")

        answer = assistant.invoke(
            {"question": user_input}, config={"callbacks": [langchain_tracer]}
        )
        logger.info(f"Answer received: {answer}")

        assert (
            expected_category.lower() in answer.lower()
        ), f"expected: {expected_category}, got {answer}"

        if expected_subjects:
            subjects_found = [
                subject
                for subject in expected_subjects
                if subject.lower() in answer.lower()
            ]
            logger.info(f"Subjects found in response: {subjects_found}")

            assert any(
                subject.lower() in answer.lower() for subject in expected_subjects
            ), f"Expected the assistant questions to include '{expected_subjects}', but got {answer}"


# Run all tests if script is executed directly
if __name__ == "__main__":
    print("Running all tests with pytest...\n")
    # Run all tests in this file
    pytest.main(["-v", __file__])

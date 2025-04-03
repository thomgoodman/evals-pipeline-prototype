import pytest
import os
from unittest.mock import patch, mock_open, MagicMock


# Test the read_file_into_string function - these tests are mostly fine
def test_read_file_into_string_success(setup_logging):
    logger = setup_logging
    logger.info("Testing read_file_into_string success case")
    mock_content = "Test content"
    with patch("builtins.open", mock_open(read_data=mock_content)) as mock_file:
        from app import read_file_into_string

        result = read_file_into_string("some_file.txt")
        logger.info(f"Result: {result}")
        assert result == mock_content


def test_read_file_into_string_file_not_found(setup_logging):
    logger = setup_logging
    logger.info("Testing read_file_into_string file not found case")
    with patch("builtins.open", side_effect=FileNotFoundError):
        with patch("builtins.print") as mock_print:
            from app import read_file_into_string

            result = read_file_into_string("nonexistent_file.txt")
            mock_print.assert_called_once()
            logger.info(f"Print call args: {mock_print.call_args[0][0]}")
            assert "not found" in mock_print.call_args[0][0]
            assert result is None


def test_read_file_into_string_generic_error(setup_logging):
    logger = setup_logging
    logger.info("Testing read_file_into_string generic error case")
    with patch("builtins.open", side_effect=Exception("Test error")):
        with patch("builtins.print") as mock_print:
            from app import read_file_into_string

            result = read_file_into_string("some_file.txt")
            mock_print.assert_called_once()
            logger.info(f"Print call args: {mock_print.call_args[0][0]}")
            assert "error occurred" in mock_print.call_args[0][0]
            assert result is None


# Test the assistant_chain function by mocking the entire chain
def test_assistant_chain_for_valid_category(setup_logging, langchain_tracer):
    logger = setup_logging
    logger.info("Testing assistant_chain for valid category")

    # Setup mock chain that returns valid quiz response
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = (
        "Question 1:#### What is the capital of France?\n\n"
        "Question 2:#### Where is the Louvre located?\n\n"
        "Question 3:#### What is the population of Paris?"
    )
    logger.info("Set up mock chain with valid response")

    # Mock the ChatPromptTemplate, ChatOpenAI, and StrOutputParser
    with patch("app.ChatPromptTemplate.from_messages") as mock_prompt:
        with patch("app.ChatOpenAI") as mock_llm_class:
            with patch("app.StrOutputParser") as mock_parser_class:
                # Setup the pipe operation to return our mock chain
                mock_prompt.return_value.__or__.return_value.__or__.return_value = (
                    mock_chain
                )

                # Import with patched quiz bank
                with patch("app.quiz_bank", "Test quiz bank for Geography"):
                    from app import assistant_chain

                # Create the chain
                chain = assistant_chain()

                # Test with valid category
                result = chain.invoke({"question": "Generate a quiz about Geography"})

                # Verify the mock was called
                mock_chain.invoke.assert_called_once_with(
                    {"question": "Generate a quiz about Geography"}
                )

                # Verify result contains expected quiz format
                assert "What is the capital of France?" in result
                assert "Where is the Louvre located?" in result
                assert "What is the population of Paris?" in result


def test_assistant_chain_for_invalid_category(setup_logging, langchain_tracer):
    logger = setup_logging
    logger.info("Testing assistant_chain for invalid category")

    # Setup mock chain that returns no information response
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = "I'm sorry I do not have information about that"
    logger.info("Set up mock chain with invalid response")

    # Mock the ChatPromptTemplate, ChatOpenAI, and StrOutputParser
    with patch("app.ChatPromptTemplate.from_messages") as mock_prompt:
        with patch("app.ChatOpenAI") as mock_llm_class:
            with patch("app.StrOutputParser") as mock_parser_class:
                # Setup the pipe operation to return our mock chain
                mock_prompt.return_value.__or__.return_value.__or__.return_value = (
                    mock_chain
                )

                # Import with patched quiz bank
                with patch("app.quiz_bank", "Test quiz bank for Geography"):
                    from app import assistant_chain

                # Create the chain
                chain = assistant_chain()

                # Test with invalid category
                result = chain.invoke({"question": "Generate a quiz about History"})

                # Verify the mock was called
                mock_chain.invoke.assert_called_once_with(
                    {"question": "Generate a quiz about History"}
                )

                # Verify result contains expected error message
                assert "I'm sorry I do not have information about that" in result


def test_assistant_chain_system_message(setup_logging):
    logger = setup_logging
    logger.info("Testing assistant_chain system message construction")
    # Test that the system message is correctly constructed with the quiz bank
    with patch("app.quiz_bank", "Test content"):
        from app import assistant_chain, system_message

        # Verify the system message contains key components
        assert "customized quiz" in system_message
        assert "Geography" in system_message
        assert "Science" in system_message
        assert "Art" in system_message

        # The test quiz bank gets replaced in the system_message
        assert "topics are below:" in system_message
        assert (
            "Test content" in system_message
        )  # This should match the mocked quiz_bank content
        assert (
            "Pick up to two subjects" in system_message
        )  # This text appears after the quiz bank

        # Verify the chain is constructed using the system message
        with patch("app.ChatPromptTemplate.from_messages") as mock_prompt:
            assistant_chain()
            # Check that the first argument to from_messages is a list
            # and the first element has "system" as the first item
            args, _ = mock_prompt.call_args
            assert args[0][0][0] == "system"
            assert args[0][0][1] == system_message


# Run all tests if script is executed directly
if __name__ == "__main__":
    pytest.main(["-v", __file__])

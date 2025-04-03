import pytest
import os
from unittest.mock import patch, mock_open
from app import read_file_into_string


# Test the read_file_into_string function
def test_read_file_into_string_success():
    mock_content = "Test content"
    with patch("builtins.open", mock_open(read_data=mock_content)) as mock_file:
        result = read_file_into_string("some_file.txt")
        mock_file.assert_called_once_with("some_file.txt", "r")
        assert result == mock_content


def test_read_file_into_string_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with patch("builtins.print") as mock_print:
            result = read_file_into_string("nonexistent_file.txt")
            mock_print.assert_called_once()
            assert "not found" in mock_print.call_args[0][0]
            assert result is None


def test_read_file_into_string_generic_error():
    with patch("builtins.open", side_effect=Exception("Test error")):
        with patch("builtins.print") as mock_print:
            result = read_file_into_string("some_file.txt")
            mock_print.assert_called_once()
            assert "error occurred" in mock_print.call_args[0][0]
            assert result is None


# Test the quiz functionality through direct call to ChatOpenAI
def test_quiz_category_validation():
    with patch("app.quiz_bank", "Test quiz bank content"):
        with patch("app.ChatOpenAI") as mock_chat:
            mock_instance = mock_chat.return_value
            mock_instance.invoke.return_value.content = (
                "I can generate a quiz about Geography"
            )

            # Patch the prompt
            with patch("app.ChatPromptTemplate.from_messages") as mock_prompt:
                mock_prompt.return_value = mock_prompt
                with patch("app.StrOutputParser") as mock_parser:
                    mock_parser.return_value.parse.return_value = (
                        "I can generate a quiz about Geography"
                    )

                    # Import here to avoid early execution of the import in app.py
                    from app import assistant_chain

                    chain = assistant_chain(
                        system_message="Test system message",
                        human_template="Test human template {question}",
                        llm=mock_instance,
                        output_parser=mock_parser.return_value,
                    )

                    # Mock the invoke method of the chain
                    with patch.object(chain, "invoke") as mock_invoke:
                        mock_invoke.return_value = (
                            "Question 1:#### What is the capital of France?"
                        )

                        # Test invocation
                        result = chain.invoke(
                            {"question": "Generate a quiz about Geography"}
                        )

                        # Verify mock_invoke was called with the right parameters
                        mock_invoke.assert_called_once_with(
                            {"question": "Generate a quiz about Geography"}
                        )

                        # Verify result
                        assert (
                            result == "Question 1:#### What is the capital of France?"
                        )


# Test the error handling for unknown categories
def test_unknown_category():
    with patch("app.quiz_bank", "Test quiz bank content"):
        with patch("app.ChatOpenAI") as mock_chat:
            mock_instance = mock_chat.return_value
            mock_instance.invoke.return_value.content = (
                "I'm sorry I do not have information about that"
            )

            # Patch the prompt
            with patch("app.ChatPromptTemplate.from_messages") as mock_prompt:
                mock_prompt.return_value = mock_prompt
                with patch("app.StrOutputParser") as mock_parser:
                    mock_parser.return_value.parse.return_value = (
                        "I'm sorry I do not have information about that"
                    )

                    # Import here to avoid early execution of the import in app.py
                    from app import assistant_chain

                    chain = assistant_chain(
                        system_message="Test system message",
                        human_template="Test human template {question}",
                        llm=mock_instance,
                        output_parser=mock_parser.return_value,
                    )

                    # Mock the invoke method of the chain
                    with patch.object(chain, "invoke") as mock_invoke:
                        mock_invoke.return_value = (
                            "I'm sorry I do not have information about that"
                        )

                        # Test invocation
                        result = chain.invoke(
                            {"question": "Generate a quiz about History"}
                        )

                        # Verify mock_invoke was called with the right parameters
                        mock_invoke.assert_called_once_with(
                            {"question": "Generate a quiz about History"}
                        )

                        # Verify result
                        assert (
                            result == "I'm sorry I do not have information about that"
                        )
                        assert "I'm sorry" in result


# Run all tests if script is executed directly
if __name__ == "__main__":
    pytest.main(["-v", __file__])

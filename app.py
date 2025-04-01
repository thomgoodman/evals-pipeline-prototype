from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
_ = load_dotenv(find_dotenv())

delimiter = "####"


def read_file_into_string(file_path):
    try:
        with open(file_path, "r") as file:
            file_content = file.read()
            return file_content
    except FileNotFoundError:
        print(f"The file at '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


quiz_bank = read_file_into_string("quiz_bank.txt")

system_message = f"""
Follow these steps to generate a customized quiz for the user.
The question will be delimited with four hashtags i.e {delimiter}

The user will provide a category that they want to create a quiz for. Any questions included in the quiz
should only refer to the category.

Step 1:{delimiter} First identify the category user is asking about from the following list:
* Geography
* Science
* Art

Step 2:{delimiter} Determine the subjects to generate questions about. The list of topics are below:

{quiz_bank}

Pick up to two subjects that fit the user's category. For example, if the user asks about Geography, you should use the Paris subject since it is explicitly labeled with the Geography category.

Step 3:{delimiter} Generate a quiz for the user. Based on the selected subjects generate 3 questions for the user using the facts about the subject.

Use the following format for the quiz:
Question 1:{delimiter} <question 1>

Question 2:{delimiter} <question 2>

Question 3:{delimiter} <question 3>

Additional rules:

- Only use explicit matches for the category, if the category is not an exact match to categories in the quiz bank, answer that you do not have information.
- If the user asks about a valid category (Geography, Science, or Art) but there are no subjects with that category in the quiz bank, answer "I'm sorry I do not have information about that".
- If the user asks about a subject not in the quiz bank, answer "I'm sorry I do not have information about that".
"""

"""
  Helper functions for writing the test cases
"""


def assistant_chain(
    system_message=system_message,
    human_template="{question}",
    llm=ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
    ),
    output_parser=StrOutputParser(),
):

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("human", human_template),
        ]
    )
    return chat_prompt | llm | output_parser

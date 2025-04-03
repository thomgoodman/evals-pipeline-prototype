import pytest
import logging
from langchain.callbacks.tracers.stdout import ConsoleCallbackHandler


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """Set up logging for all tests"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger()


@pytest.fixture(scope="function")
def langchain_tracer():
    """Return a ConsoleCallbackHandler for LangChain tracing"""
    return ConsoleCallbackHandler()

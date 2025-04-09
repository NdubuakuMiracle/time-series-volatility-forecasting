"""This module extracts information from the `.env` file so that
AlphaVantage API key can be used in other parts of the project.
"""

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)


class Settings(BaseSettings):
    """
    Settings class for configuring the project.
    This class uses Pydantic's BaseSettings to define and validate the configuration settings
    required for the project. The settings include:
    Attributes:
        alpha_api_key (str): API key for Alpha Vantage.
    The configuration is loaded from a .env file specified in the inner Config class.
    Example:
        To use the settings, create an instance of the Settings class:
        settings = Settings()
        print(settings.alpha_api_key)
    """

    """Uses pydantic to define settings for project."""

    alpha_api_key: str

    class Config:
        env_file = ".env"


# Create instance of `Settings` class that will be imported
settings = Settings()

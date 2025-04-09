import os

class Settings:
    alpha_api_key = os.getenv("alpha_api_key")
    
settings = Settings()

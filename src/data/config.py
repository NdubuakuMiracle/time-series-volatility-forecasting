import os

class Settings:
    alpha_api_key = os.getenv("ALPHA_API_KEY")
    
settings = Settings()

class Settings:
    APP_NAME = "NexridgeTech"

    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/nexridgetech"

    JWT_SECRET = "super-secret-key"

    JWT_ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 60


settings = Settings()
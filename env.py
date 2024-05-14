import os
from dotenv import dotenv_values, load_dotenv


class Env:
    env: dict[str, str | None] = {
        **dotenv_values(".env.example"),
        **dotenv_values(".env")
    }

    @staticmethod
    def load_environment(path: str):
        load_dotenv(path)
        Env.env = {**Env.env, **os.environ}

    @staticmethod
    def get(key: str):
        return Env.env.get(key)

    @staticmethod
    def get_strict[T](key: str, type_: type[T]) -> T:
        env_var = Env.env.get(key)
        if (env_var is None):
            raise ValueError(f"Environment variable {key} not found")
        try:
            return type_(env_var)
        except:
            raise ValueError("Environment variable IMAGE_TARGET_SIZE is wrong")

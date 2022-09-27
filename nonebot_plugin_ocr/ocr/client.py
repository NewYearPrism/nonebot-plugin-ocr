import abc

from pydantic import BaseModel


class Result(abc.ABC, BaseModel, extra='ignore'):
    @abc.abstractmethod
    def get_words(self) -> list[str]:
        pass

    def to_string(self) -> str:
        return self.json()


class Error(abc.ABC, BaseModel, extra='ignore'):
    @abc.abstractmethod
    def get_error_message(self) -> str:
        pass

    def to_string(self) -> str:
        return self.json()


class Client(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def parse_content(result: str) -> Result | Error | None:
        pass

    @abc.abstractmethod
    async def ocr_by_httpurl(self, http_url: str, **param) -> str:
        pass

    @abc.abstractmethod
    async def ocr_by_base64image(self, b64_image: str, **param) -> str:
        pass

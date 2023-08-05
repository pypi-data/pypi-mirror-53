import typing
from abc import ABCMeta, abstractmethod, abstractproperty


class CredentialProvider(metaclass=ABCMeta):
    @abstractproperty
    def provider_code(self) -> str:
        pass

    @abstractmethod
    def get_credential(self, identifier: str) -> typing.Any:
        pass


class CredentialProviderManager:
    @staticmethod
    def get_by_code(code: str) -> typing.Union[CredentialProvider, None]:
        for provider in CredentialProvider.__subclasses__():
            if provider.provider_code == code:
                return provider


# Simple example with Vault by HashiCorp
"""
from ..config import get_config
import hvac

class VaultProvider(CredentialProvider):
    provider_code = "vault"

    def __init__(self, token: str) -> None:
        self.client = hvac.Client(url=get_config("vault_url"))
        self.client.token = get_config("vault_token")

    def get_credential(self, identifier: str) -> typing.Dict[str, typing.Any]:
        return self.client.read(identifier)["data"]
"""

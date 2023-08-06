from datasetmaker import clients
from datasetmaker.models import Client


def create_client(source: str) -> Client:
    return clients.available[source]()  # type: ignore

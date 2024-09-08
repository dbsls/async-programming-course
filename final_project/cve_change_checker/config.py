from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Project settings
    concurrent_requests: int = 10

    # CVE settings
    cve_path: str
    delta_json_url: str = "https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/delta.json"
    cve_api_endpoint: str = "http://host.docker.internal:8080/items/"
    fetch_timeout: int = 3
    schedule_interval: int = 300


def get_settings():
    return Settings()

import httpx
from urllib.parse import urlparse
from src.auxiliary.utils import logger

GITHUB_API = "https://api.github.com"


def parse_repo(url: str):
    path = urlparse(url).path.strip("/")
    parts = path.split("/")
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL")
    return parts[0], parts[1]


async def fetch_repository_bundle(repo_url: str):
    owner, repo = parse_repo(repo_url)

    async with httpx.AsyncClient() as client:
        logger.info(f"Call httpx.AsyncClient: owner={owner}, repo={repo}")
        meta_resp = await client.get(f"{GITHUB_API}/repos/{owner}/{repo}")
        logger.info(f"Status Code = {meta_resp.status_code}")
        if meta_resp.status_code != 200:
            raise ValueError("Repository not found")

        readme_resp = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/readme",
            headers={"Accept": "application/vnd.github.raw"},
        )

        languages_resp = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/languages"
        )

        tree_resp = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
        )

    return {
        "metadata": meta_resp.json(),
        "readme": readme_resp.text if readme_resp.status_code == 200 else "",
        "languages": list(languages_resp.json().keys())
        if languages_resp.status_code == 200
        else [],
        "files": [f["path"] for f in tree_resp.json().get("tree", [])],
    }

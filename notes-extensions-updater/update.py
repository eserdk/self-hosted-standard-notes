import asyncio
import datetime
import json
import logging
import shutil
import time
import zipfile
from pathlib import Path
from typing import Dict, List, Optional

import aiofiles
import httpx
import yaml
from environs import Env

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO
)
logger = logging.getLogger()

env = Env()

GH_USERNAME = env.str("GH_USERNAME")
GH_TOKEN = env.str("GH_TOKEN")
HOST = env.str("HOST", "http://localhost:81")

BASE_DIR = Path(__file__).parent
EXTENSIONS_DIR = BASE_DIR / "extensions"
PUBLIC_DIR = BASE_DIR / "public"

if not PUBLIC_DIR.exists():
    PUBLIC_DIR.mkdir()


class Extension:
    info: Optional[Dict] = None
    zipfile: Optional[Path] = None
    version: str

    def __init__(
        self,
        id_: str,
        name: str,
        content_type: str,
        repo: str,
        main: str,
        description: Optional[str] = None,
        marketing_url: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        flags: Optional[List] = None,
        dock_icon: Optional[str] = None,
        layerable: Optional[str] = None,
        area: Optional[str] = None,
    ):
        self.id_ = id_
        self.name = name
        self.repo = repo
        self.main = main
        self.content_type = content_type
        self.description = description
        self.marketing_url = marketing_url
        self.thumbnail_url = thumbnail_url
        self.flags = flags
        self.dock_icon = dock_icon
        self.layerable = layerable
        self.area = area

        self.repo_dir = PUBLIC_DIR / self.repo.split("/")[-1]

    @classmethod
    def from_metadata(cls, metadata: Dict) -> "Extension":
        return Extension(
            id_=metadata["id"],
            name=metadata["name"],
            content_type=metadata["content_type"],
            area=metadata.get("area"),
            description=metadata.get("description"),
            marketing_url=metadata.get("marketing_url"),
            thumbnail_url=metadata.get("thumbnail_url"),
            flags=metadata.get("flags"),
            dock_icon=metadata.get("dock_icon"),
            layerable=metadata.get("layerable"),
            repo=metadata["github"],
            main=metadata["main"],
        )

    def to_dict(self) -> Dict:
        dict_ = {
            "identifier": self.id_,
            "name": self.name,
            "content_type": self.content_type,
            "area": self.area,
            "version": self.version,
            "description": self.description,
            "url": "/".join(
                (
                    HOST,
                    "extensions",
                    self.repo.split("/")[-1],
                    self.version,
                    self.main,
                )
            ),
            "download_url": f"https://github.com/{self.repo}/archive/{self.version}.zip",
            "marketing_url": self.marketing_url,
            "thumbnail_url": self.thumbnail_url,
            "valid_until": (
                datetime.datetime.utcnow() + datetime.timedelta(days=365 * 10)
            ).isoformat(timespec="milliseconds")
            + "Z",
            "latest_url": "/".join(
                (HOST, "extensions", self.repo.split("/")[-1], "index.json")
            ),
            "flags": self.flags,
            "dock_icon": self.dock_icon,
            "layerable": self.layerable,
        }

        return {k: v for k, v in dict_.items() if v}


async def download_extension(
    github_client: httpx.AsyncClient, extension: Extension
) -> None:
    # download release info
    response = await github_client.get(f"/{extension.repo}/releases/latest")
    extension.info = response.json() if response.status_code == 200 else None
    if extension.info is None:
        logger.error("No info for extension with name %s. Skipping.", extension.name)
        return

    # get latest version
    extension.version = extension.info.get("tag_name")
    if extension.version is None:
        logger.error(
            "Can't find any release for extension with name %s. Skipping.",
            extension.name,
        )
        return

    # create extension directory if doesn't exist
    if not extension.repo_dir.exists():
        extension.repo_dir.mkdir()

    # create zip archive file for new release
    extension.zipfile = extension.repo_dir / f"{extension.version}.zip"
    if extension.zipfile.exists() and zipfile.is_zipfile(extension.zipfile):
        return

    extension.zipfile.touch()

    # download release
    async with httpx.AsyncClient() as client:
        async with aiofiles.open(extension.zipfile, "wb") as fp:
            async with client.stream("get", extension.info["zipball_url"]) as stream:
                async for chunk in stream.aiter_raw():
                    await fp.write(chunk)


async def download_extensions(extensions: List[Extension]) -> None:
    async with httpx.AsyncClient(
        base_url="https://api.github.com/repos", auth=(GH_USERNAME, GH_TOKEN)
    ) as client:
        await asyncio.gather(*(download_extension(client, e) for e in extensions))


def rm(file: Path) -> None:
    if file.is_dir():
        for file_ in list(file.iterdir()):
            rm(file_)
        file.rmdir()
    elif file.is_file():
        file.unlink()


def unpack(extensions: List[Extension]) -> None:
    indexes = []

    for extension in extensions:
        version_dir = extension.repo_dir / extension.version
        if version_dir.exists():
            continue

        temp_dir = extension.repo_dir / "temp"
        with zipfile.ZipFile(extension.zipfile, "r") as zf:
            zf.extractall(temp_dir)

        unarchived_dir = next(
            filter(
                lambda f: extension.repo_dir.name in f.name and f.is_dir(),
                temp_dir.iterdir(),
            )
        )
        shutil.copytree(unarchived_dir, version_dir)
        rm(temp_dir)

        index_file = extension.repo_dir / "index.json"
        if not index_file.exists():
            index_file.touch()

        index = extension.to_dict()
        index_file.write_text(json.dumps(index, indent=4))
        indexes.append(index)

    (PUBLIC_DIR / "index.json").write_text(
        json.dumps(
            {
                "content_type": "SN|Repo",
                "valid_until": (
                    datetime.datetime.utcnow() + datetime.timedelta(days=365 * 10)
                ).isoformat(timespec="milliseconds"),
                "packages": list(sorted(indexes, key=lambda i: i["name"])),
            },
            indent=4,
        )
    )


if __name__ == "__main__":
    start = time.time()
    logger.info("Extensions update started.")
    extensions = [
        Extension.from_metadata(yaml.safe_load(extension_data_file.read_text()))
        for extension_data_file in EXTENSIONS_DIR.glob("*.yaml")
    ]

    logger.info("Downloading extensions.")
    asyncio.run(download_extensions(extensions))
    logger.info("Done.")

    logger.info("Unpacking extensions.")
    unpack([e for e in extensions if e.zipfile])
    logger.info("Done.")

    logger.info("Completed in %d seconds!", time.time() - start)

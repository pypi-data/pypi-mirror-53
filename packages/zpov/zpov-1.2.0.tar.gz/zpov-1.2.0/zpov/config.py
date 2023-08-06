from typing import Dict

import attr
import ruamel.yaml
from path import Path

from .user import User


@attr.s
class Config:
    repo_path: Path = attr.ib()
    # Used to sign cookies
    secret_key: str = attr.ib()

    # Maps logins to users with names and emails
    users: Dict[str, User] = attr.ib(default={})
    public_access: bool = attr.ib(default=False)


def parse_config() -> Config:
    cfg_path = Path.getcwd() / "zpov.yml"
    parser = ruamel.yaml.YAML()
    parsed = parser.load(cfg_path.text())
    user_configs = parsed.get("users", {})
    users = {}
    for key, value in user_configs.items():
        user = User(login=key, **value)
        users[key] = user
    repo_path = Path(parsed["repo_path"])
    public_access = parsed["public_access"]
    secret_key = parsed["secret_key"]
    res = Config(
        users=users,
        repo_path=repo_path,
        public_access=public_access,
        secret_key=secret_key,
    )
    return res

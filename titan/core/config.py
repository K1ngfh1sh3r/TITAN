"""TITAN configuration models and loader."""

from pathlib import Path
from typing import Any

import yaml
from pydantic import (
    AnyHttpUrl,
    BaseModel,
    ConfigDict,
    Field,
    IPvAnyNetwork,
    field_validator,
)


class ProjectConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    environment: str = "lab"


class ProxmoxConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    endpoint: AnyHttpUrl
    node: str
    storage: str
    wan_bridge: str = "vmbr0"
    vlan_bridge: str = "vmbr1"
    verify_ssl: bool = True


class VLANConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int = Field(ge=1, le=4094)
    name: str
    subnet: IPvAnyNetwork
    purpose: str


class NetworkConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    default_deny: bool = True
    vlans: list[VLANConfig]

    @field_validator("vlans")
    @classmethod
    def validate_unique_vlans(cls, vlans: list[VLANConfig]) -> list[VLANConfig]:
        ids = [vlan.id for vlan in vlans]
        names = [vlan.name for vlan in vlans]

        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate VLAN IDs are not allowed")

        if len(names) != len(set(names)):
            raise ValueError("Duplicate VLAN names are not allowed")

        return vlans


class TITANConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project: ProjectConfig
    proxmox: ProxmoxConfig
    network: NetworkConfig


def load_config(path: Path) -> TITANConfig:
    """Load and validate a TITAN YAML configuration."""

    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with path.open("r", encoding="utf-8") as config_file:
        raw_config: Any = yaml.safe_load(config_file)

    if not isinstance(raw_config, dict):
        raise ValueError("Configuration must contain a YAML mapping")

    return TITANConfig.model_validate(raw_config)

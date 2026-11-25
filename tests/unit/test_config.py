"""Tests for TITAN configuration validation."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from titan.core.config import TITANConfig, load_config

EXAMPLE_CONFIG = Path("config/titan.example.yaml")


def test_example_configuration_loads() -> None:
    config = load_config(EXAMPLE_CONFIG)

    assert config.project.name == "ARES"
    assert config.proxmox.wan_bridge == "vmbr0"
    assert config.proxmox.vlan_bridge == "vmbr1"
    assert len(config.network.vlans) == 9


def test_vlan_ids_are_unique() -> None:
    with pytest.raises(ValidationError):
        TITANConfig.model_validate(
            {
                "project": {"name": "ARES"},
                "proxmox": {
                    "endpoint": "https://localhost:8006",
                    "node": "pve",
                    "storage": "local-lvm",
                },
                "network": {
                    "vlans": [
                        {
                            "id": 10,
                            "name": "MANAGEMENT",
                            "subnet": "10.20.10.0/24",
                            "purpose": "Administration",
                        },
                        {
                            "id": 10,
                            "name": "DEVELOPMENT",
                            "subnet": "10.20.20.0/24",
                            "purpose": "Development",
                        },
                    ]
                },
            }
        )


def test_unknown_configuration_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        TITANConfig.model_validate(
            {
                "project": {"name": "ARES"},
                "proxmox": {
                    "endpoint": "https://localhost:8006",
                    "node": "pve",
                    "storage": "local-lvm",
                    "unknown_option": True,
                },
                "network": {"vlans": []},
            }
        )

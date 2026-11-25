# TITAN

**Total Infrastructure Transformation and Automation Network**

Infrastructure Automation & Orchestration Platform.

TITAN is a Python-based orchestration platform designed to automate
the deployment, configuration, security and operation of the ARES
enterprise infrastructure on Proxmox VE.

## Project objective

The only manual operation required is the initial installation of
Proxmox VE.

After providing the initial environment configuration and credentials,
TITAN must orchestrate the complete deployment without requiring
manual intervention in Proxmox, OPNsense or the virtual machines.

## Mandatory deliverables

1. Automated Proxmox infrastructure preparation and deployment.
2. Automated OPNsense configuration through its API.
3. VLAN deployment and security policy configuration.
4. Samba Active Directory installation and configuration.
5. Automated virtual machine and service deployment.
6. WireGuard VPN deployment and configuration.
7. Monitoring and centralized logging.
8. Automated backup and restoration.
9. Professional Python command-line interface.

## Network architecture

| VLAN | Name | Network | Purpose |
|---:|---|---|---|
| 10 | MANAGEMENT | 10.20.10.0/24 | Infrastructure administration |
| 20 | DEVELOPMENT | 10.20.20.0/24 | Development workstations |
| 30 | BUSINESS | 10.20.30.0/24 | Business workstations |
| 40 | SERVERS | 10.20.40.0/24 | Internal servers |
| 50 | DMZ | 10.20.50.0/24 | Exposed services |
| 60 | MONITORING | 10.20.60.0/24 | Monitoring and logs |
| 70 | BACKUP | 10.20.70.0/24 | Backup infrastructure |
| 80 | GUEST | 10.20.80.0/24 | Guest network |
| 99 | VPN | 10.20.99.0/24 | WireGuard remote access |

OPNsense provides routing, firewalling and network segmentation.

## Technology stack

- Python: orchestration engine and CLI
- Terraform: Proxmox resource provisioning
- Ansible: operating system and service configuration
- Cloud-init: virtual machine initialization
- OPNsense API: firewall and network configuration
- Samba AD: centralized identity and DNS
- WireGuard: remote access
- Prometheus, Grafana and Loki: monitoring and logging
- Restic: backup and restoration

## Repository structure

- `titan/`: Python application and orchestration engine
- `terraform/`: infrastructure provisioning
- `ansible/`: configuration management
- `cloud-init/`: virtual machine initialization
- `config/`: environment configuration templates
- `tests/`: unit and integration tests
- `docs/`: architecture and operational documentation

## Design principles

- Automation by default
- Idempotent operations
- Secure handling of secrets
- Explicit validation and error handling
- Structured logging and traceability
- Modular and maintainable architecture
- Reproducible deployments
- Tested backup and restoration procedures

## Initial deployment workflow

1. Install Proxmox VE manually.
2. Provide TITAN with the initial environment configuration.
3. Run the TITAN deployment command.
4. Let TITAN orchestrate the infrastructure.
5. Validate the deployed environment automatically.

## Project status

**Initial repository scaffold — development not yet started.**

## Security

Never commit passwords, API tokens, private keys, Terraform state
files or environment-specific secrets to this repository.

## License

To be determined.

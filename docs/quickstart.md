# Quickstart

## General

The `netuid` for `sundara`:
* mainnet: TBD
* testnet: `130` 


### Prepare Wallet

Generally, for both validator and miner, you need to prepare your wallet and make your key registered in the subnet. You can find related guidance in the [running on mainnet](./running_on_mainnet.md) section.

If you are new to bittensor subnet, you are recommended to start by following
- [running on staging](./running_on_staging.md)
- [running on testnet](./running_on_testnet.md).

running_on_mainnet
### Install requirements

In the root folder of this repository, run the following command:
```bash
python -m pip install --no-cache-dir -e .
```

## Miner Setup

#### Install Docker

You can refer to the [docker official guide](https://docs.docker.com/engine/install/) to install docker.

In short, you can run the following command to install docker:

**Ubuntu**

```bash
# Uninstall old versionsrunning_on_testnet
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Install Docker
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# add docker permission for current user
sudo usermod -aG docker $USER
sudo systemctl enable docker

# Verify that the Docker Engine installation is successful
docker ps
```
Then you have successfully installed and started Docker Engine.

**CentOS**

```bash
# Uninstall old versions
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine

# Install the yum-utils package (which provides the yum-config-manager utility) and set up the repository
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install Docker
sudo yum install docker

# Start Docker
sudo systemctl start docker

# add docker permission for current user
sudo usermod -aG docker $USER
sudo systemctl enable docker

# Verify that the Docker Engine installation is successful
docker ps
```

Then you have successfully installed and started Docker Engine.

### Start the Miner

You can start the miner by running the following command:

```bash
python neurons/miner.py --netuid 130 --subtensor.network test --wallet.name miner --wallet.hotkey default --logging.debug --blacklist.force_validator_permit  --engine.name ollama --engine.models llama2,mistral
```

## Validator Setup

You may need to setup your wallet and hotkey according to [running on testnet](./docs/running_on_testnet.md).

### Start the Validator

You can start the miner by running the following command:

```bash
 python neurons/validator.py --netuid 130 --subtensor.network test --wallet.name miner --wallet.hotkey default --logging.debug

```

## Gateway Setup

You may need to setup your wallet and hotkey according to [running on testnet](./docs/running_on_testnet.md).

Gateway allows you to access the subnet and do inference call from external network.

A validator hotkey is required for running the gateway.

### Start the Gateway

You can start the miner by running the following command:

```bash
 python gateway/gateway.py --netuid 130 --subtensor.network test --wallet.name validator --wallet.hotkey default --logging.debug 

```
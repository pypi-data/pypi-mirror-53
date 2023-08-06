# Breqwatr Deployment Tool


## Install

### From PyPi

```python
pip install breqwatr-deployment-tool
```

### From GitHub

```python
pip install git+https://github.com/breqwatr/breqwatr-deployment-tool.git
```


## Examples

### Help

```bash
bwdt --help
```

### Configuration

This defines if you're doing an online/offline install.

```bash
# Online Example
bwdt configure --key-id <key ID> --key <key> --online

# Offline Example
bwdt configure --offline --offline-path <directory of offline files>
```

### Registry

Start the registry service

```bash
bwdt registry start
```

Sync an OpenStack image from Breqwatr's upstream online registry to a  locally
hosted registry.

```bash
bwdt registry sync-openstack-image <registry url> <image name>
```

Sync all the required images for an OpenStack deployment to a local registry.

```bash
bwdt registry sync-all-openstack-images <registry url>
```

List the images in a local registry and their tags

```bash
bwdt registry list-images <registry url>
```

### Launch PXE

Example of launching the PXE service:

```bash
bwdt pxe start --interface enp0s25 --dhcp-start 10.1.0.90 --dhcp-end 10.1.0.99
```

### Ansible

The Ansible service is used to deploy OpenStack onto the servers.
The `--kolla-dir` path helps to keep the files generated on the host.

```bash
mkdir -p /etc/kolla
bwdt ansible start \
  --ssh-key-path <path to id_rsa> \
  --cloud-yml-path <path to cloud.yml> \
  --kolla-dir /etc/kolla
```

The `bwdt ansible` commands can also interact within the container.

```bash
# generate kolla config
bwdt ansible openstack gen-config

# bootstrap the servers
bwdt ansible openstack bootstrap
```

### Apt

To deploy a private APT server:

```bash
bwdt apt start
```

### Pip

To launch a private Pip repo for python

```bash
bwdt pip start
```


### Arcus

Arcus is the custom web UI Breqwatr uses to replace Horizon.

Initialize the datbase for the Arcus service:

```bash
bwdt arcus database-init --host <host> --admin-user root --admin-pass <password> --arcus-pass <password>
```

Create the Openstack service account for Arcus:

```bash
bwdt arcus create-service-account --cloud-fqdn <fqdn or vip> --bootstrap-password <password of bootstrap user> --sa-password <password for arcus SA>
```

Start the Arcus API service

```bash
bwdt arcus api start \
  --openstack-fqdn <fqdn or vip for openstack> \
  --sql-ip <database IP or FQDN> \
  --sql-password <db password for arcus user> \
  --rabbit-ip <server ip addr 1> --rabbit-ip <server 2> --rabbit-ip <server 3> \
  --rabbit-pass <rabbitmq openstack user password>
```

Start the Arcus Client

```bash
bwdt arcus client start \
  --openstack-ip <vip or fqdn to openstack> \
  --api-ip <vip or fqdn of arcus-api>
```

Start the Arcus Mgr

arcus-mgr needs Kolla-Ansible's files to do some things like repairing Mariadb
when it goes down. Distribute those files to the control nodes first.

```bash
# From the Deployment Server
bwdt ansible transfer-kolla-dir --server-ip <ip address>

# On the OpenStack control node
bwdt arcus mgr start \
  --kolla-dir <directory of Kolla files> \
  --openstack-ip <vip or fqdn of openstack> \
  --rabbit-ip <server ip addr 1> --rabbit-ip <server 2> --rabbit-ip <server 3> \
  --rabbit-pass <rabbitmq openstack user password> \
  --sql-ip <database IP address> \
  --sql-password <arcus user password for database>
```


## Docker Utilities

### Pull images from the upstream registry

This one's mostly for troubleshooting / advanced users

```bash
# Pull one image
bwdt docker pull breqwatr/pxe --tag 7.0

# Pull all images
bwdt docker pull-all
```

### Export image to disk

Useful for building offline installer media

```bash
# make a directory to export to
mkdir -p /Volumes/Breqwatr7/images/

# export one image
bwdt docker export-image \
  --tag '7.0' \
  --repository 'breqwatr/pxe' \
  -o '/Volumes/Breqwatr7/images/'

# export all images to build the offline installer media
bwdt docker export-image-all -o '/Volumes/Breqwatr7/images/'
```

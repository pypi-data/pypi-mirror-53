# Breqwatr Deployment Tool

The Breqwatr deployment tool is a toolkit for deploying Breqwatr OpenStack and
its accompanying services. The Breqwatr Deployment Tool is accessed from the
command line of an Ubuntu based OS using the command `bwdt`.

BWDT requires Docker, and either a removable drive provided by Breqwatr for
offline installs or a special key and ID for configuring the tool to pull files
and images from the upstream servers.


## Installation

### From PyPi

```bash
pip install breqwatr-deployment-tool
```

### From GitHub

```bash
pip install git+https://github.com/breqwatr/breqwatr-deployment-tool.git
```

### From Offline Media

The offline media will contain a file named `bwdt.tar.gz`. Unpack it to a
directory off of the removable media, then install with this command:

```bash
pip install --no-index --find-links <directory>  breqwatr-deployment-tool
```

---


# Features

## Help

```bash
bwdt --help
```


## Configuration

Breqwatr deployment tool supports both offline and online installations.
```bash
# Online Example
bwdt configure --key-id <key ID> --key <key> --online

# Offline Example
bwdt configure --offline --offline-path <directory of offline files>
```


## Docker Registry

### Start Registry
Launch a local Docker registry container

```bash
bwdt registry start
```

### Sync Images to Registry
Sync an OpenStack image from Breqwatr's upstream online registry to a  locally
hosted registry.

```bash
bwdt registry sync-openstack-image <registry url> <image name>
```

Sync all the required images for an OpenStack deployment to a local registry.

```bash
bwdt registry sync-all-openstack-images <registry url>
```

### List Images in Registry
List the images in a local registry and their tags

```bash
bwdt registry list-images <registry url>
```


## Ubuntu Apt

BWDT can deploy an optional private Apt service. This allows servers to run the
`apt-get` command to install software when they don't have an internet
connection.

The Breqwatr Apt container is not a complete mirror, but it does contain all
the required packages to deploy OpenStack along with some other useful ones.

The private Apt service also provides a mechanism to limit
OpenStack servers to the Ubuntu packages which Breqwatr has tested, ensuring
the stability of Breqwatr clouds.

### Start Apt Container

```bash
bwdt apt start
```


## Python Pip

Similar to the Apt container, BWDT can deploy a private Pip service.


### Start Pip Container

```bash
bwdt pip start
```


## PXE

BWDT can launch a PXE service based on DNSMasq and Nginx to enable fast,
offline installation of Ubuntu 18.04 on remote servers.

### Start PXE Container

```bash
bwdt pxe start --interface enp0s25 --dhcp-start 10.1.0.90 --dhcp-end 10.1.0.99
```


## Ansible

The Ansible service is used to deploy OpenStack and supporting tools.

### Start Ansible Container

The `--kolla-dir` path helps to keep the files generated on the host.

```bash
mkdir -p /etc/kolla
bwdt ansible start \
  --ssh-key-path <path to id_rsa> \
  --cloud-yml-path <path to cloud.yml> \
  --kolla-dir /etc/kolla
```

### Deploy Openstack

The Ansible container leverages some open source Ansible libraries which often
take a long time to run. For that reason, these bwdt commands print
`docker exec` commands which need to be ran. Surrounding the commands with the
`$()` will make them auto-execute.


```bash
# generate kolla config
$(bwdt ansible openstack gen-config)

# bootstrap the servers
$(bwdt ansible openstack bootstrap)

# Deploy openstacl
$(bwdt ansible openstack deploy)

# Post-deploy
$(bwdt ansible openstack post-deploy)
```



### Arcus

Arcus is Breqwatr's custom web UI, API, and cloud management daemon. Among
other uses, Arcus is a drop-in replacement of OpenStack Horizon.

### Initialize the Datbase

```bash
bwdt arcus database-init --host <host> --admin-user root --admin-pass <password> --arcus-pass <password>
```

### Create the Openstack service account

```bash
bwdt arcus create-service-account --cloud-fqdn <fqdn or vip> --bootstrap-password <password of bootstrap user> --sa-password <password for arcus SA>
```

### Start the Arcus API service

```bash
bwdt arcus api start \
  --openstack-fqdn <fqdn or vip for openstack> \
  --sql-ip <database IP or FQDN> \
  --sql-password <db password for arcus user> \
  --rabbit-ip <server ip addr 1> --rabbit-ip <server 2> --rabbit-ip <server 3> \
  --rabbit-pass <rabbitmq openstack user password>
```

### Start the Arcus Client

```bash
bwdt arcus client start \
  --openstack-ip <vip or fqdn to openstack> \
  --glance-https \
  --api-ip <vip or fqdn of arcus-api> \
  --arcus-https \
  --cert-path <path to HTTPS certificate file>
  --cert-key-path <path to HTTPS certificate private key file>

```

### Start the Arcus Mgr

The Arcus Mgr needs Kolla-Ansible's files to do some things like repairing
Mariadb when it goes down. Distribute those files to the control nodes first.

Also ensure the Arcus Manager has an SSH key which is authorized to each
OpenStack server.

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
  --sql-password <arcus user password for database> \
  --ssh-key-path <authorized SSH key>
```


---

# Docker Utilities

## Build Offline Installation Media

To build your own offline install media on a USB stick for a dark-site cloud:

```bash
bwdt export-offline-media <path>
```

## Download Cloud Config Template

To download a template cloud configuration for use with the Ansible container:

```bash
bwdt download cloud-yml <path>
```

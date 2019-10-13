# Ceph
Ceph is a fucking amazing distributed, replicated and fault-tolerant storage system. 
This playbook installs a working Ceph cluster on a bunch of CentOS7 nodes, using a CentOS7-based deployment node.

## Prerequisites

1. A deployment node where this playbook will run. 
2. Nodes for hosting Ceph OSDs and MONs with root access over SSH. 

## Installation

1. Clone this repository and install its dependencies:
```
git clone https://github.com/rudimk/eurus-fabric-playbooks.git
cd eurus-fabric-playbooks
pip install -r requirements.txt
```

2. On the deployment node, update yum and install Python 3.6:
```
yum update
yum install centos-release-scl
yum install rh-python36
```

3. To activate Python 3, you need to use scl to activate a new shell which uses Python 3 instead of the default Python 2 installation(yeah, CentOS is fucked up). Run the command below whenever you need to run the playbook(you could also put it in your `.bashrc` or `.bash_profile`):
```
scl enable rh-python36 bash
```

4. Ensure that the nodes you intend to deploy Ceph on are accessible from the deployment node. Also make sure you can log into these nodes over SSH without a password. Here's a quick primer on creating a new keypair and setting up password-less SSH auth:
    
    a. Create a new keypair without a passphrase:
    ```
    ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
    ```
    Try giving a different name for this particular keypair, to differentiate it from other keypairs. Here, we'll use `id_rsa_ceph` as an example.

    b. Create a SSH config file at `~/.ssh/config` with the following entries(one entry per Ceph node):
    ```
    Host <NODE_IP>
    	IdentityFile ~/.ssh/id_rsa_ceph
    ```
    c. One disadvantage with running Python 3 inside a separate shell with `scl` is that you need to manually add the SSH keypair to the SSH agent on the deployment node. To take care of that:
    ```
    eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_rsa_ceph
    ```

5. Finally, it's time to populate the inventory file. Open `ceph/centos7/inventory.py` and fill in the following details:

    a. First, enter a list of Ceph node hostnames in the CEPH_NODES variable, along with their IP addresses and the volumes you wish to use as Ceph OSDs. Here's an example:
    ```
    CEPH_NODES = [{'hostname': 'ceph01', 'ip': '10.0.0.1', 
	'volumes': ['/dev/sdb', '/dev/sdc']}, {'hostname': 'ceph02', 'ip': '10.0.0.2', 
	'volumes': ['/dev/sdb', '/dev/sdc']}]
    ``` 
    Ensure that the hostnames mentioned here match the actual hostnames of the Ceph nodes, as defined in the `/etc/hostname` file on every node. Also, ensure that the volumes mentioned here are simply attached to the node, and are not mounted or formatted as `ext4` or `XFS` volumes - you can find the volume paths by running `fdisk -l` on each Ceph node.

    b. Next, define a list of hosts that will be injected into the `/etc/hosts` file on the deployment machine as well as on all Ceph nodes. Here's a sample:
    ```
    HOST_ENTRIES = """

    10.0.0.1	ceph01
    10.0.0.2	ceph02

    """
    ```
    Again, ensure that the hostnames and IPs mentioned here match those in CEPH_NODES, as well as the actual hostnames/IPs of the nodes you're planning to use.

    c. Finally, specify an admin username and password, which will be used to configure authenticated access to the Ceph dashboard.
    ```
    CEPH_ADMIN_USERNAME = "admin"
    CEPH_ADMIN_PASSWORD = "password"
    ```

6. Now you're all set. Navigate into the `ceph` directory and fire up `main.py`:
```
cd ceph/centos7
python main.py
```

The installer will create a Ceph configuration at `/root/CEPH-CLUSTER`, and install a Ceph cluster on your nodes. It will also configure the Ceph dashboard - you can view it at `http://ACTIVE_CEPH_NODE:8080`.


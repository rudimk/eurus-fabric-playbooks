# K3s

K3s is a terrific Kubernetes distribution from Rancher Labs which uses 40MB worth of system resources - ideal for edge deployments. But it's also perfect for running full-scale Kubernetes clusters due to its simplicity. 

This playbook installs a working K3s cluster with a single master node and multiple worker nodes running Ubuntu 18.04, using a deployment node running CentOS 7.

## Prerequisites

1. A deployment node where this playbook will run. 
2. Nodes for hosting K3s master and worker components with root access over SSH.

## Installation

2. Clone this repository and install its dependencies:
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

4. Ensure that the nodes you intend to deploy K3s on are accessible from the deployment node. Also make sure you can log into these nodes over SSH without a password. Here's a quick primer on creating a new keypair and setting up password-less SSH auth:
    
    a. Create a new keypair without a passphrase:
    ```
    ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
    ```
    Try giving a different name for this particular keypair, to differentiate it from other keypairs. Here, we'll use `id_rsa_k3s` as an example.

    b. Create a SSH config file at `~/.ssh/config` with the following entries(one entry per K3s node):
    ```
    Host <NODE_IP>
    	IdentityFile ~/.ssh/id_rsa_k3s
    ```
    c. One disadvantage with running Python 3 inside a separate shell with `scl` is that you need to manually add the SSH keypair to the SSH agent on the deployment node. To take care of that:
    ```
    eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_rsa_k3s
    ```

5. Finally, it's time to populate the inventory file. Open `k3s/ubuntu18/inventory.py` and fill in the following details:
    
    a. Provide the hostname and IP address of the master node in `K3S_MASTER_NODE`: `K3S_MASTER_NODE = {'hostname': 'k3s-master', 'ip': '10.1.0.1'}`.

    b. Provide hostnames and IP addresses for your worker nodes:
    ```
    K3S_WORKER_NODES = [{'hostname': 'k3s-worker-1', 'ip': '10.1.0.2'}, {'hostname': 'k3s-worker-2', 'ip': '10.1.0.3'}]
    ```

    c. Finally, define a list of hosts that will be injected into the `/etc/hosts` file on the deployment machine as well as on all K3s nodes. Here's a sample:
    ```

    10.1.0.1	k3s-master
    10.1.0.2	k3s-worker-1
    10.1.0.3	k3s-worker-2
    
    ```
    Ensure that the hostnames and IPs mentioned here match those in `K3S_MASTER_NODE` and `K3S_WORKER_NODES`, as well as the actual hostnames/IPs of the nodes you're planning to use.

6. Now you're all set. Navigate to the `k3s/ubuntu18` directory and fire up `main.py`:
```
cd k3s/ubuntu18
python main.py
```

7. The installer will deploy a K3s cluster on your nodes, and download a `kubeconfig.yaml` file to `/root` on your deployment machine. Modify the `server` variable in the file to `https://<K3S_MASTER_HOSTNAME>:6443`. Install `kubectl` and configure it to interact with your new cluster:
```
yum install -y kubectl
mkdir -p /root/.kube
cp /root/kubeconfig.yaml /root/.kube/config
```

8. Verify your cluster is operational and reachable:
```
kubectl get nodes
```


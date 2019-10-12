import inventory


def addLocalHosts(conn, logging):
	logging.info(f"[X] Adding master and worker nodes to the /etc/hosts file on the local machine ==>")
	addHost = conn.run(f"cat << EOM >> /etc/hosts \n {inventory.HOST_ENTRIES} \n")
	logging.info("[X] Added hosts to the local machine.")


def addRemoteHosts(hostname, conn, logging):
	logging.info(f"[X] Adding master and worker nodes to the /etc/hosts file on {hostname} ==>")
	addHost = conn.run(f"cat << EOM >> /etc/hosts \n {inventory.HOST_ENTRIES} \n")
	logging.info(f"[X] Added hosts to the /etc/hosts file on {hostname}.")


def updatePackages(hostname, conn, logging):
	logging.info(f"[X] Updating apt packages on {hostname} ==>")
	conn.run("apt update")
	logging.info(f"Updated apt packages on {hostname}.")


def installK3sMaster(hostname, conn, logging):
	logging.info(f"[X] Deploying k3s master on {hostname} ==>")
	conn.run("curl -sfL https://get.k3s.io | sh -")
	k3sToken = conn.run("cat /var/lib/rancher/k3s/server/node-token").stdout.strip()
	logging.info(f"[X] K3S Agent Token: {k3sToken}")
	conn.get(remote="/etc/rancher/k3s/k3s.yaml", local="/root/kubeconfig.yaml")
	logging.info("[X Downloaded the cluster's kubeconfig to /root/kubeconfig.yaml.")
	return k3sToken


def installK3sWorker(hostname, conn, masterHostName, k3sToken, logging):
	logging.info(f"[X] Deploying the k3s worker agent on {hostname} ==>")
	conn.run(f"curl -sfL https://get.k3s.io | K3S_URL=https://{masterHostName}:6443 K3S_TOKEN={k3sToken} sh -")
	logging.info(f"Deployed k3s worker agent on {hostname}.")
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
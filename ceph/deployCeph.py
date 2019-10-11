

def initialiseCephConfig(conn, hostnames, logging):
	logging.info("Initialising Ceph cluster configuration on the local machine ==>")
	conn.local("mkdir /root/CEPH-CLUSTER")
	conn.local(f"cd /root/CEPH-CLUSTER && ceph-deploy new {hostnames}")
	logging.info("Initialised Ceph cluster configuration on the local machine.")


def installCephBinaries(conn, hostnames, logging):
	logging.info(f"[X] Installing Ceph binaries on all nodes ==>")
	conn.local(f"cd /root/CEPH-CLUSTER && ceph-deploy install {hostnames}")
	logging.info("Installed Ceph binaries on all nodes.")





def initialiseCephConfig(conn, hostnames, logging):
	logging.info("Initialising Ceph cluster configuration on the local machine ==>")
	conn.local("mkdir /root/CEPH-CLUSTER")
	conn.local(f"cd /root/CEPH-CLUSTER && ceph-deploy new {hostnames}")
	logging.info("Initialised Ceph cluster configuration on the local machine.")

from fabric import Connection
import inventory
import logging

logging.basicConfig(level=logging.DEBUG)

def getConnection(node):
	return Connection(host=node, user='root', key_filename=inventory.SSH_KEY)


def setupNTP():
	for node in inventory.CEPH_NODES:
		conn = getConnection(node)
		logging.info(f"[X] Setting up NTP on {node} ==>")
		setNTPServer = conn.run('ntpdate -s time.nist.gov')
		updateYum = conn.run('yum update -y')
		installNTP = conn.run('yum install -y ntp')
		enableNTPD = conn.run('systemctl enable ntpd')
		startNTPD = conn.run('systemctl start ntpd')
	logging.info("[X] Finished setting up NTPD.")


def addHosts():
	for node in inventory.CEPH_NODES:
		conn = getConnection(node)
		logging.info(f"[X] Adding Ceph nodes to the /etc/hosts file on {node} ==>")
		addHost = conn.run(f"cat << EOM >> /etc/hosts \n {inventory.HOST_ENTRIES} \n")
	logging.info("[X] Added hosts.")





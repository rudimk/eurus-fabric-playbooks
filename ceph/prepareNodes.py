from fabric import Connection
import inventory
import logging

logging.basicConfig(level=logging.DEBUG)

def getConnection(node):
	return Connection(host=node, user='root', key_filename=inventory.SSH_KEY)


def setupNTP():
	for node in inventory.CEPH_NODES:
		conn = getConnection(node)
		logging.info("[X] Setting up NTP on {node}".format(node=node))
		setNTPServer = conn.run('ntpdate -s time.nist.gov')
		updateYum = conn.run('yum update -y')
		installNTP = conn.run('yum install -y ntp')
		enableNTPD = conn.run('systemctl enable ntpd')
		startNTPD = conn.run('systemctl start ntpd')
	logging.info("[X] Finished setting up NTPD.")






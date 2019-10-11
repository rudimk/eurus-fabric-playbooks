from fabric import Connection
import inventory
import logging

import prepareNodes

logging.basicConfig(level=logging.DEBUG)

def getRemoteConnection(hostname):
	return Connection(host=hostname, user='root', key_filename=inventory.SSH_KEY)

def getLocalConnection():
	return Connection(host='localhost')

if __name__ == '__main__':
	prepareNodes.addLocalHosts(getLocalConnection(), logging)
	prepareNodes.setupRepos(getLocalConnection(), logging)
	for node in inventory.CEPH_NODES:
		conn = getRemoteConnection(node['hostname'])
		prepareNodes.setupNTP(node, conn, logging)
		prepareNodes.addRemoteHosts(node, conn, logging)

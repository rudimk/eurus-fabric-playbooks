from fabric import Connection
import inventory
import logging

import prepareNodes

logging.basicConfig(level=logging.DEBUG)

def getRemoteConnection(node):
	return Connection(host=node, user='root', key_filename=inventory.SSH_KEY)

def getLocalConnection():
	return Connection(host='localhost')

if __name__ == '__main__':
	prepareNodes.setupRepos(conn, logging)
	for node in inventory.CEPH_NODES:
		conn = getRemoteConnection(node)
		prepareNodes.setupNTP(node, conn, logging)
		prepareNodes.addHosts(node, conn, logging)

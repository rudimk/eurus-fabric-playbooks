from fabric import Connection
import inventory
import logging

import k3sCluster

logging.basicConfig(level=logging.DEBUG)

def getRemoteConnection(hostname):
	return Connection(host=hostname, user='root')

def getLocalConnection():
	return Connection(host='localhost')

if __name__ == '__main__':
	logging.info("[X] Initialising K3s deployment ==>")
	k3sCluster.addLocalHosts(getLocalConnection(), logging)
	k3sCluster.addRemoteHosts(getRemoteConnection(inventory.K3S_MASTER_NODE['hostname']))
	for node in inventory.K3S_WORKER_NODES:
		k3sCluster.addRemoteHosts(getRemoteConnection(node['hostname']))
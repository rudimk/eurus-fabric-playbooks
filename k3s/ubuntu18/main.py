from fabric import Connection
import inventory
import logging

import k3sCluster

logging.basicConfig(level=logging.INFO)

def getRemoteConnection(hostname):
	return Connection(host=hostname, user='root')

def getLocalConnection():
	return Connection(host='localhost')

if __name__ == '__main__':
	logging.info("[X] Initialising K3s deployment ==>")
	k3sCluster.addLocalHosts(getLocalConnection(), logging)
	k3sCluster.addRemoteHosts(inventory.K3S_MASTER_NODE['hostname'], getRemoteConnection(inventory.K3S_MASTER_NODE['hostname']), logging)
	k3sCluster.updatePackages(inventory.K3S_MASTER_NODE['hostname'], getRemoteConnection(inventory.K3S_MASTER_NODE['hostname']), logging)
	for node in inventory.K3S_WORKER_NODES:
		k3sCluster.addRemoteHosts(node['hostname'], getRemoteConnection(node['hostname']), logging)
		k3sCluster.updatePackages(node['hostname'], getRemoteConnection(node['hostname']), logging)
	k3sToken = k3sCluster.installK3sMaster(inventory.K3S_MASTER_NODE['hostname'], getRemoteConnection(inventory.K3S_MASTER_NODE['hostname']), logging)
	for node in inventory.K3S_WORKER_NODES:
		k3sCluster.installK3sWorker(node['hostname'], getRemoteConnection(node['hostname']), inventory.K3S_MASTER_NODE['hostname'], k3sToken, logging)
	logging.info("[X] Finished deploying k3s cluster.")
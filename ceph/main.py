from fabric import Connection
import inventory
import logging

import prepareNodes
import deployCeph

logging.basicConfig(level=logging.DEBUG)

def getRemoteConnection(hostname):
	return Connection(host=hostname, user='root', key_filename=inventory.SSH_KEY)

def getLocalConnection():
	return Connection(host='localhost')

def getHostString():
	hostnames = ""
	for node in inventory.CEPH_NODES:
		hostnames += node['hostname'] + ' '
	return hostnames

if __name__ == '__main__':
	prepareNodes.addLocalHosts(getLocalConnection(), logging)
	prepareNodes.setupRepos(getLocalConnection(), logging)
	for node in inventory.CEPH_NODES:
		conn = getRemoteConnection(node['hostname'])
		prepareNodes.setupNTP(node['hostname'], conn, logging)
		prepareNodes.addRemoteHosts(node['hostname'], conn, logging)
	deployCeph.initialiseCephConfig(getLocalConnection(), getHostString(), logging)
	deployCeph.installCephBinaries(getLocalConnection(), getHostString(), logging)
	deployCeph.installCephMon(getLocalConnection(), logging)
	deployCeph.installCephAdmin(getLocalConnection(), getHostString(), logging)
	for node in inventory.CEPH_NODES:
		conn = getRemoteConnection(node['hostname'])
		deployCeph.syncNTP(node['hostname'], conn, logging)
	deployCeph.installCephManager(getLocalConnection(), getHostString(), logging)
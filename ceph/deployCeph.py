import time
import inventory

def initialiseCephConfig(conn, hostnames, logging):
	logging.info("Initialising Ceph cluster configuration on the local machine ==>")
	conn.local("mkdir /root/CEPH-CLUSTER")
	conn.local(f"cd /root/CEPH-CLUSTER && ceph-deploy new {hostnames}")
	logging.info("Initialised Ceph cluster configuration on the local machine.")


def installCephBinaries(conn, hostnames, logging):
	logging.info("[X] Installing Ceph binaries on all nodes ==>")
	conn.local(f"cd /root/CEPH-CLUSTER && ceph-deploy install {hostnames}")
	logging.info("Installed Ceph binaries on all nodes.")


def installCephMon(conn, logging):
	logging.info("[X] Installing Ceph MONs on all nodes ==>")
	conn.local("cd /root/CEPH-CLUSTER && ceph-deploy mon create-initial")
	logging.info("Installed Ceph MONs on all nodes.")


def installCephAdmin(conn, hostnames, logging):
	logging.info("[X] Installing Ceph admin components on all nodes ==>")
	conn.local(f"cd /root/CEPH-CLUSTER && ceph-deploy admin {hostnames}")
	logging.info("Installed Ceph admin components on all nodes.")


def syncNTP(hostname, conn, logging):
	logging.info(f"[X] Shutting down ntpd on {hostname} ==>")
	conn.run("systemctl stop ntpd")
	logging.info(f"[X] Updating timserver pool on {hostname} ==>")
	conn.run("ntpdate -s time.nist.gov; ntpdate -s time.nist.gov; ntpdate -s time.nist.gov")
	logging.info(f"[X] Restarting ntpd on {hostname} ==>")
	conn.run("systemctl restart ntpd")
	logging.info(f"[X] Waiting for 10 seconds before restarting Ceph components on {hostname} ==>")
	time.sleep(10)
	logging.info(f"[X] Restarting Ceph components on {hostname} ==>")
	conn.run("systemctl restart ceph.target")
	logging.info(f"[X] Completed NTP sync on {hostname}.")


def installCephManager(conn, hostnames, logging):
	logging.info("[X] Installing Ceph MGRs on all nodes ==>")
	conn.local(f"cd /root/CEPH-CLUSTER && ceph-deploy mgr create {hostnames}")
	logging.info("[X] Installed Ceph MGRs on all nodes.")


def installCephOSD(hostname, conn, volumes, logging):
	logging.info(f"[X] Initialising OSD creation on {hostname} ==>")
	for volume in volumes:
		logging.info(f"[X] Creating Ceph OSD on {hostname}:{volume} ==>")
		conn.local(f"cd /root/CEPH-CLUSTER && ceph-deploy osd create --data {volume} {hostname}")
		logging.info(f"[X] Deployed Ceph OSD on {hostname}:{volume}.")
	logging.info(f"[X] Deployed Ceph OSDs on {hostname}.")


def configureCephDashboard(hostname, ip, conn, logging):
	logging.info(f"[X] Configuring Ceph dashboard on {hostname} ==>")
	conn.run("ceph config set mgr mgr/dashboard/ssl false")
	conn.run("ceph mgr module enable dashboard")
	conn.run(f"ceph dashboard set-login-credentials {inventory.CEPH_ADMIN_USERNAME} {inventory.CEPH_ADMIN_PASSWORD}")
	logging.info("[X] Configured the Ceph admin dashboard. Access it at http://{ip}:8080.")
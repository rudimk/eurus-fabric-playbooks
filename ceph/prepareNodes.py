import inventory

CEPH_REPO = """

[ceph-noarch]
name=Ceph noarch packages
baseurl=https://download.ceph.com/rpm-$release/el7/noarch
enabled=1
gpgcheck=1
type=rpm-md
gpgkey=https://download.ceph.com/keys/release.asc

"""


def addLocalHosts(conn, logging):
	logging.info(f"[X] Adding Ceph nodes to the /etc/hosts file on the local machine ==>")
	addHost = conn.run(f"cat << EOM >> /etc/hosts \n {inventory.HOST_ENTRIES} \n")
	logging.info("[X] Added hosts to the local machine.")


def setupRepos(conn, logging):
	logging.info("[X] Adding the Ceph repos to the local machine ==>")
	addRepos = conn.local(f"release=mimic && cat << EOM >> /etc/yum.repos.d/ceph.repo \n {CEPH_REPO} \n")
	updateRepos = conn.local("yum update -y")
	installPythonSetuptools = conn.local("yum install -y python-setuptools")
	installCephDeploy = conn.local("yum install ceph-deploy -y")
	logging.info("[X] Added the Ceph repos, and installed ceph-deploy.")


def setupNTP(hostname, conn, logging):
	logging.info(f"[X] Setting up NTP on {hostname} ==>")
	updateYum = conn.run("yum update -y")
	installNTPDate = conn.run("yum install -y ntpdate")
	setNTPServer = conn.run('ntpdate -s time.nist.gov')
	logging.debug(setNTPServer.stdout)
	updateYum = conn.run('yum update -y')
	installNTP = conn.run('yum install -y ntp')
	enableNTPD = conn.run('systemctl enable ntpd')
	startNTPD = conn.run('systemctl start ntpd')
	logging.info(f"[X] Finished setting up NTPD on {hostname}.")


def addRemoteHosts(hostname, conn, logging):
	logging.info(f"[X] Adding Ceph nodes to the /etc/hosts file on {hostname} ==>")
	addHost = conn.run(f"cat << EOM >> /etc/hosts \n {inventory.HOST_ENTRIES} \n")
	logging.info(f"[X] Added hosts to the /etc/hosts file on {hostname}.")









CEPH_REPO = """

[ceph-noarch]
name=Ceph noarch packages
baseurl=https://download.ceph.com/rpm-$release/el7/noarch
enabled=1
gpgcheck=1
type=rpm-md
gpgkey=https://download.ceph.com/keys/release.asc

"""


def setupNTP(node, conn, logging):
	logging.info(f"[X] Setting up NTP on {node} ==>")
	setNTPServer = conn.run('ntpdate -s time.nist.gov')
	updateYum = conn.run('yum update -y')
	installNTP = conn.run('yum install -y ntp')
	enableNTPD = conn.run('systemctl enable ntpd')
	startNTPD = conn.run('systemctl start ntpd')
	logging.info("[X] Finished setting up NTPD.")


def addHosts(node, conn, logging):
	conn = getRemoteConnection(node)
	logging.info(f"[X] Adding Ceph nodes to the /etc/hosts file on {node} ==>")
	addHost = conn.run(f"cat << EOM >> /etc/hosts \n {inventory.HOST_ENTRIES} \n")
	logging.info("[X] Added hosts.")


def setupRepos(conn, logging):
	logging.info("[X] Adding the Ceph repos to the local machine ==>")
	addRepos = conn.local(f"release=mimic && cat << EOM >> /etc/yum.repos.d/ceph.repo \n {CEPH_REPO} \n")
	updateRepos = conn.local("yum update -y")
	installCephDeploy = conn.local("yum install ceph-deploy -y")
	logging.info("[X] Added the Ceph repos, and installed ceph-deploy.")








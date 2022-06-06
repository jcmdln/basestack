Capstone is an Ansible playbook that deploys OpenStack and Ceph on Podman.

NOTE: This project isn't ready yet! Sorry!

There are many great ways to deploy OpenStack. Capstone seeks to fill a
distinct niche for DevOps ilk by acting as a framework for deploying evaluation
and production clusters with as little cognitive overhead and prior knowledge
as possible. To this end, Capstone provides a somewhat rigid configuration with
few knobs so that referring to "Capstone" means something concrete. Once your
needs are not fulfilled by the general-purpose nature of Capstone, you are
encouraged to fork and modify the familiarly structured Ansible Playbook and
port changes as best suits your needs.

# Using

```
$ sudo dnf install -y podman
$ sudo setenforce 0
$ sudo mkdir -m 0750 /etc/capstone /var/log/capstone
$ sudo chown $USER:$USER -R /etc/capstone /var/log/capstone
$ virtualenv .venv
$ source .venv/bin/activate
(.venv) $ pip install -r requirements.txt
(.venv) $ ansible-galaxy collection install --upgrade -r requirements.yaml
(.venv) $ ansible-playbook -i inventory/localhost.yaml site.yaml --list-tags

playbook: site.yaml

  play #1 (all): Prepare        TAGS: [always]
      TASK TAGS: [always]

  play #2 (all): Depends        TAGS: [depends]
      TASK TAGS: [build, ceph, ceph-build, ceph-config, ceph-deploy, config,
      depends, depends-build, depends-config, depends-deploy, deploy, postgres,
      postgres-build, postgres-config, postgres-deploy, rabbitmq,
      rabbitmq-build, rabbitmq-config, redis, redis-build, redis-config]

  play #3 (all): OS Core        TAGS: [os-core]
      TASK TAGS: [build, config, keystone, keystone-build, keystone-config,
      os-core]

  play #4 (all): OS Extras      TAGS: [os-extras]
      TASK TAGS: [build, config, openstackclient, openstackclient-build,
      openstackclient-config, os-extras]
```

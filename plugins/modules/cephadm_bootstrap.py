#!/usr/bin/python
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, annotations

from ansible.module_utils.basic import AnsibleModule


class Result:
    changed: bool = False
    command: str = "cephadm"
    msg: str = "no action performed"
    rc: int = 0
    stderr: str = ""
    stdout: str = ""


def deploy(m: AnsibleModule) -> Result:
    r: Result = Result()

    r.command = f"{r.command} deploy {m.params['fsid']} {m.params['name']}"
    if m.params["name"] == "osd":
        r.command = f"{r.command} --osd-fsid {m.params['osd_fsid']}"
    if m.params["config"]:
        r.command = f"{r.command} --config {m.params['config']}"
    if m.params["config_json"]:
        r.command = f"{r.command} --config-json {m.params['config_json']}"
    if m.params["key"]:
        r.command = f"{r.command} --key {m.params['key']}"
    if m.params["keyring"]:
        r.command = f"{r.command} --keyring {m.params['keyring']}"
    if m.params["allow_ptrace"]:
        r.command = f"{r.command} --allow-ptrace"
    if m.params["reconfig"]:
        r.command = f"{r.command} --reconfig"
    if m.params["skip_firewalld"]:
        r.command = f"{r.command} --skip-firewalld"

    r.rc, r.stdout, r.stderr = m.run_command(r.command, check_rc=False)
    if r.rc > 0:
        r.changed = True
        r.msg = "received a non-zero exit code"

    return r


def rm_daemon(m: AnsibleModule) -> Result:
    r: Result = Result()

    r.command = f"{r.command} rm-daemon {m.params['fsid']} {m.params['name']}"
    if m.params["force"]:
        r.command = f"{r.command} --force" % r.command
    if m.params["force_delete_data"]:
        r.command = f"{r.command} --force-delete-data" % r.command

    r.rc, r.stdout, r.stderr = m.run_command(r.command, check_rc=False)
    if r.rc > 0:
        r.changed = True
        r.msg = "received a non-zero exit code"

    return r


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "allow_ptrace": {"type": "bool", "default": False},
            "config": {"type": "str", "default": ""},
            "config_json": {"type": "mapping", "default": ""},
            "force": {"type": "bool", "default": False},
            "force_delete_data": {"type": "bool", "default": False},
            "fsid": {"type": "str", "required": True},
            "key": {"type": "str", "default": ""},
            "keyring": {"type": "str", "default": ""},
            "name": {
                "type": "str",
                "choices": [
                    "alertmanager",
                    "crash",
                    "grafana",
                    "iscsi",
                    "mgr",
                    "mon",
                    "nfs",
                    "node-exporter",
                    "osd",
                    "prometheus",
                    "rbd-mirror",
                    "rgw",
                ],
                "required": True,
            },
            "osd_fsid": {"type": "str", "default": ""},
            "reconfig": {"type": "bool", "default": False},
            "skip_firewalld": {"type": "bool", "default": False},
            "state": {"type": "str", "choices": ["absent", "present"], "required": True},
        },
        mutually_exclusive=[
            ["allow_ptrace", "force"],
            ["allow_ptrace", "force_delete_data"],
        ],
        required_if=[["name", "osd", ["osd_fsid"]]],
    )

    if module.params["state"] == "absent":
        result = rm_daemon(module)
    else:
        result = deploy(module)

    if result.rc > 0:
        module.fail_json(**result)
    else:
        module.exit_json(**result)


if __name__ == "__main__":
    main()

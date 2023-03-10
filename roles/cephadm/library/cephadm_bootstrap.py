#!/usr/bin/python
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, annotations

from ansible.module_utils.basic import AnsibleModule


class Result:
    changed: bool = False
    command: str = "cephadm bootstrap"
    msg: str = "no action performed"
    rc: int = 0
    stderr: str = ""
    stdout: str = ""


def cephadm_bootstrap(module: AnsibleModule) -> Result:
    r: Result = Result()

    if not module.params["mon_ip"]:
        r.rc = 1
        r.msg = "'mon_ip' cannot be an empty string."
        return r
    else:
        r.command = "{} --mon-ip {}".format(r.command, module.params["mon_ip"])

    if module.params["allow_fqdn_hostname"]:
        r.command = "{} --allow-fqdn-hostname".format(r.command)
    if module.params["allow_overwrite"]:
        r.command = "{} --allow-overwrite".format(r.command)
    if module.params["config"]:
        r.command = "{} --config {}".format(r.command, module.params["config"])
    if module.params["fsid"]:
        r.command = "{} --fsid {}".format(r.command, module.params["fsid"])
    if module.params["mgr_id"]:
        r.command = "{} --mgr-id {}".format(r.command, module.params["mgr_id"])
    if module.params["mon_addrv"]:
        r.command = "{} --mon-addrv {}".format(r.command, module.params["mon_addrv"])
    if module.params["mon_id"]:
        r.command = "{} --mon-id {}".format(r.command, module.params["mon_id"])
    if module.params["no_minimize_config"]:
        r.command = "{} --no-minimize-config".format(r.command)
    if module.params["orphan_initial_daemons"]:
        r.command = "{} --orphan-initial-daemons".format(r.command)
    if module.params["output_config"]:
        r.command = "{} --output-config {}".format(r.command, module.params["output_config"])
    if module.params["output_dir"]:
        r.command = "{} --output-dir {}".format(r.command, module.params["output_dir"])
    if module.params["output_keyring"]:
        r.command = "{} --output-keyring {}".format(r.command, module.params["output_keyring"])
    if module.params["output_pub_ssh_key"]:
        r.command = "{} --output-pub-ssh-key {}".format(r.command, module.params["output_pub_ssh_key"])

    if module.params["skip_dashboard"]:
        r.command = "{} --skip-dashboard".format(r.command)
    else:
        if module.params["dashboard_crt"]:
            r.command = "{} --dashboard-crt {}".format(r.command, module.params["dashboard_crt"])
        if module.params["dashboard_key"]:
            r.command = "{} --dashboard-key {}".format(r.command, module.params["dashboard_key"])
        if module.params["dashboard_password_noupdate"]:
            r.command = "{} --dashboard-password-noupdate".format(r.command)
        if module.params["initial_dashboard_user"]:
            r.command = "{} --initial-dashboard-user {}".format(r.command, module.params["initial_dashboard_user"])
        if module.params["initial_dashboard_password"]:
            r.command = "{} --initial-dashboard-password {}".format(
                r.command, module.params["initial_dashboard_password"]
            )

    if module.params["skip_firewalld"]:
        r.command = "{} --skip-firwalld".format(r.command)
    if module.params["skip_mon_network"]:
        r.command = "{} --skip-mon-network".format(r.command)
    if module.params["skip_monitoring_stack"]:
        r.command = "{} --skip-monitoring-stack".format(r.command)
    if module.params["skip_ping_check"]:
        r.command = "{} --skip-ping-check".format(r.command)
    if module.params["skip_prepare_host"]:
        r.command = "{} --skip-prepare-host".format(r.command)
    if module.params["skip_pull"]:
        r.command = "{} --skip-pull".format(r.command)
    if module.params["skip_ssh"]:
        r.command = "{} --skip-ssh".format(r.command)

    r.rc, r.stdout, r.stderr = module.run_command(r.command, check_rc=False)

    if r.rc > 0:
        r.changed = True
        r.msg = "received a non-zero exit code"

    return r


def main() -> None:
    module = AnsibleModule(
        argument_spec=dict(
            allow_fqdn_hostname={"type": "bool", "default": False},
            allow_overwrite={"type": "bool", "default": False},
            config={"type": "str", "default": ""},
            dashboard_crt={"type": "str", "default": ""},
            dashboard_key={"type": "str", "default": ""},
            dashboard_password_noupdate={"type": "bool", "default": False},
            fsid={"type": "str", "default": ""},
            initial_dashboard_user={"type": "str", "default": ""},
            initial_dashboard_password={"type": "str", "default": ""},
            mgr_id={"type": "str", "default": ""},
            mon_addrv={"type": "str", "default": ""},
            mon_id={"type": "str", "default": ""},
            mon_ip={"type": "str", "required": True},
            no_minimize_config={"type": "bool", "default": False},
            orphan_initial_daemons={"type": "bool", "default": False},
            output_config={"type": "str", "default": ""},
            output_dir={"type": "str", "default": ""},
            output_keyring={"type": "str", "default": ""},
            output_pub_ssh_key={"type": "str", "default": ""},
            skip_dashboard={"type": "bool", "default": False},
            skip_firewalld={"type": "bool", "default": False},
            skip_mon_network={"type": "bool", "default": False},
            skip_monitoring_stack={"type": "bool", "default": False},
            skip_ping_check={"type": "bool", "default": False},
            skip_prepare_host={"type": "bool", "default": False},
            skip_pull={"type": "bool", "default": False},
            skip_ssh={"type": "bool", "default": False},
        ),
        mutually_exclusive=[
            ["skip_dashboard", "dashboard_crt"],
            ["skip_dashboard", "dashboard_key"],
            ["skip_dashboard", "dashboard_password_noupdate"],
            ["skip_dashboard", "initial_dashboard_user"],
            ["skip_dashboard", "initial_dashboard_password"],
        ],
    )

    result: Result = cephadm_bootstrap(module)
    if result.rc > 0:
        module.fail_json(**result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()

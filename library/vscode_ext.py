from __future__ import annotations

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = ""
EXAMPLES = ""
RETURN = ""


def get_installed(module: AnsibleModule) -> dict[str, str]:
    ret, stdout, stderr = module.run_command([
        "code",
        "--list-extensions",
        "--show-versions",
    ])
    return dict(
        line.split("@")
        for line in stdout.splitlines()
    )


def install_extension(
    module: AnsibleModule,
    name: str,
    *,
    version: str | None = None,
) -> bool:
    cmd = ["code", "--install-extension", name]

    if version is not None:
        cmd[-1] += f"@{version}"

    cmd.append("--force")
    _, stdout, _ = module.run_command(cmd)

    return "is already installed" not in stdout


def remove_extension(
    module: AnsibleModule,
    name: str,
) -> bool:
    ret, _, _ = module.run_command(["code", "--uninstall-extension", name])
    return not ret


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "name": {
                "type": "str",
                "required": True,
            },
            "state": {
                "type": "str",
                "default": "present",
                "choices": ["present", "latest", "absent"],
            },
            "version": {
                "type": "str",
            },
        },
    )

    params = module.params
    installed = get_installed(module)
    changed = False

    if (
        (params["state"] == "present" and params["name"] not in installed)
        or params["state"] == "latest"
    ):
        changed = install_extension(
            module,
            params["name"],
            version=params["version"] or None,
        )
    elif params["state"] == "absent" and params["name"] in installed:
        changed = remove_extension(module, params["name"])

    module.exit_json(**{"changed": changed})


if __name__ == "__main__":
    main()

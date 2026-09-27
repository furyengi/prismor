"""Effective policy mode shown by ``prismor status``."""

from types import SimpleNamespace

from prismor.runtime.cli import _status_effective_mode


def test_org_policy_mode_overrides_hook_install_mode():
    engine = SimpleNamespace(
        workspace_managed=True,
        device_mode="enforce",
        default_mode="observe",
        remote_policy_meta={"profile_name": "Production", "version": 3},
    )

    assert _status_effective_mode("observe", engine) == (
        "enforce",
        'org policy "Production" v3',
    )


def test_org_policy_default_mode_is_used_without_device_override():
    engine = SimpleNamespace(
        workspace_managed=True,
        device_mode=None,
        default_mode="enforce",
        remote_policy_meta={"version": 4},
    )

    assert _status_effective_mode("observe", engine) == ("enforce", "org policy v4")


def test_unmanaged_workspace_keeps_hook_mode():
    engine = SimpleNamespace(
        workspace_managed=False,
        device_mode="enforce",
        default_mode="enforce",
        remote_policy_meta={"profile_name": "Production", "version": 3},
    )

    assert _status_effective_mode("observe", engine) == ("observe", None)

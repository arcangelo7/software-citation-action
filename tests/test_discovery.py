# SPDX-FileCopyrightText: 2026 Arcangelo Massari <github@a.arcangelomassari.com>
#
# SPDX-License-Identifier: ISC

from __future__ import annotations

from pathlib import Path

import pytest

from software_citation_sync.config import ProjectMetadata
from software_citation_sync.discovery import discover_project_metadata, discover_version


def test_discover_version_requires_package_json_version(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text('{"name": "ramose"}', encoding="utf-8")

    with pytest.raises(KeyError) as exc_info:
        discover_version(tmp_path)

    assert exc_info.value.args == ("version",)


def test_discover_project_metadata_from_pyproject(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        "\n".join(
            [
                "[project]",
                'name = "ramose"',
                'version = "2.8.0"',
                'authors = [{ name = "Arcangelo Massari", email = "github@a.arcangelomassari.com" }]',
                "",
            ],
        ),
        encoding="utf-8",
    )

    assert discover_project_metadata(tmp_path) == ProjectMetadata(
        title="ramose",
        authors=("Arcangelo Massari",),
    )

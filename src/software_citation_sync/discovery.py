# SPDX-FileCopyrightText: 2026 Arcangelo Massari <github@a.arcangelomassari.com>
#
# SPDX-License-Identifier: ISC

from __future__ import annotations

import json
from pathlib import Path
from typing import cast

import tomlkit
from tomlkit.items import Table

from software_citation_sync.config import ProjectMetadata


def discover_version(root: Path) -> str | None:
    package_json = root / "package.json"
    pyproject_toml = root / "pyproject.toml"
    if package_json.exists():
        data: object = json.loads(package_json.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            msg = "package.json must contain a JSON object"
            raise TypeError(msg)
        package = cast("dict[str, object]", data)
        version = package["version"]
        if not isinstance(version, str):
            msg = "package.json `version` must be a string"
            raise TypeError(msg)
        return str(version)
    if pyproject_toml.exists():
        data = tomlkit.parse(pyproject_toml.read_text(encoding="utf-8"))
        project = data["project"]
        if not isinstance(project, Table):
            msg = "pyproject.toml `[project]` must be a table"
            raise TypeError(msg)
        version = project["version"]
        if not isinstance(version, str):
            msg = "pyproject.toml `project.version` must be a string"
            raise TypeError(msg)
        return str(version)
    return None


def discover_project_metadata(root: Path) -> ProjectMetadata | None:
    package_json = root / "package.json"
    pyproject_toml = root / "pyproject.toml"
    if package_json.exists():
        return _discover_package_json_metadata(package_json)
    if pyproject_toml.exists():
        return _discover_pyproject_metadata(pyproject_toml)
    return None


def _discover_package_json_metadata(path: Path) -> ProjectMetadata:
    data: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        msg = "package.json must contain a JSON object"
        raise TypeError(msg)
    package = cast("dict[str, object]", data)
    title = package["name"]
    if not isinstance(title, str):
        msg = "package.json `name` must be a string"
        raise TypeError(msg)
    return ProjectMetadata(title=str(title), authors=_package_json_authors(package))


def _discover_pyproject_metadata(path: Path) -> ProjectMetadata:
    data = tomlkit.parse(path.read_text(encoding="utf-8"))
    project = data["project"]
    if not isinstance(project, Table):
        msg = "pyproject.toml `[project]` must be a table"
        raise TypeError(msg)
    title = project["name"]
    if not isinstance(title, str):
        msg = "pyproject.toml `project.name` must be a string"
        raise TypeError(msg)
    return ProjectMetadata(title=str(title), authors=_pyproject_authors(project))


def _package_json_authors(package: dict[str, object]) -> tuple[str, ...]:
    if "author" in package:
        return (_package_json_author_name(package["author"]),)
    contributors = package["contributors"]
    if not isinstance(contributors, list):
        msg = "package.json `contributors` must be an array"
        raise TypeError(msg)
    return tuple(_package_json_author_name(contributor) for contributor in contributors)


def _package_json_author_name(author: object) -> str:
    if isinstance(author, str):
        return str(author)
    if not isinstance(author, dict):
        msg = "package.json authors must be strings or objects"
        raise TypeError(msg)
    author_data = cast("dict[str, object]", author)
    name = author_data["name"]
    if not isinstance(name, str):
        msg = "package.json author `name` must be a string"
        raise TypeError(msg)
    return str(name)


def _pyproject_authors(project: Table) -> tuple[str, ...]:
    authors = project["authors"]
    if not isinstance(authors, list):
        msg = "pyproject.toml `project.authors` must be an array"
        raise TypeError(msg)
    return tuple(_pyproject_author_name(author) for author in authors)


def _pyproject_author_name(author: object) -> str:
    if not isinstance(author, dict):
        msg = "pyproject.toml authors must be tables"
        raise TypeError(msg)
    author_data = cast("dict[str, object]", author)
    name = author_data["name"]
    if not isinstance(name, str):
        msg = "pyproject.toml author `name` must be a string"
        raise TypeError(msg)
    return str(name)

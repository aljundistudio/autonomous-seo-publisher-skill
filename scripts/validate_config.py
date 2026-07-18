#!/usr/bin/env python3
"""Validate an autonomous-seo-publisher configuration without dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

PROVIDERS = {
    "openrouter", "gemini", "openai", "anthropic", "local", "custom",
    "openrouter-images", "gemini-image", "openai-images", "media-library", "none",
}
RASTER_FORMATS = {"png", "jpeg", "jpg", "webp"}
SECRET_VALUE = re.compile(r"^(?:sk-|AIza|xai-|ghp_|Bearer\s)", re.IGNORECASE)

def nested(data: dict, dotted: str):
    value = data
    for key in dotted.split("."):
        if not isinstance(value, dict) or key not in value:
            raise KeyError(dotted)
        value = value[key]
    return value

def find_plaintext_secrets(value, path=""):
    issues = []
    if isinstance(value, dict):
        for key, item in value.items():
            item_path = f"{path}.{key}" if path else key
            lowered = key.lower()
            if lowered in {"api_key", "apikey", "token", "access_token", "secret"} and isinstance(item, str) and item:
                issues.append(f"{item_path} must reference a secret, not contain one")
            if isinstance(item, str) and SECRET_VALUE.match(item.strip()):
                issues.append(f"{item_path} appears to contain a plaintext credential")
            issues.extend(find_plaintext_secrets(item, item_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            issues.extend(find_plaintext_secrets(item, f"{path}[{index}]"))
    return issues

def validate(data: dict):
    errors = []
    warnings = []
    required = [
        "version", "site.id", "site.base_url", "site.brand", "site.languages", "site.timezone",
        "schedule.time", "schedule.max_posts_per_local_date",
        "providers.text.type", "providers.text.model",
        "providers.image.type", "publishing.mode", "safeguards.lock_file",
    ]
    for field in required:
        try:
            nested(data, field)
        except KeyError:
            errors.append(f"missing required field: {field}")

    if errors:
        return errors, warnings

    base_url = str(nested(data, "site.base_url"))
    parsed = urlparse(base_url)
    if parsed.scheme != "https" or not parsed.netloc:
        errors.append("site.base_url must be an absolute HTTPS URL")

    languages = nested(data, "site.languages")
    if not isinstance(languages, list) or not languages or any(not isinstance(item, str) or not item.strip() for item in languages):
        errors.append("site.languages must be a non-empty string array")

    schedule = str(nested(data, "schedule.time"))
    if not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", schedule):
        errors.append("schedule.time must use 24-hour HH:MM format")

    max_posts = nested(data, "schedule.max_posts_per_local_date")
    if max_posts != 1:
        warnings.append("schedule.max_posts_per_local_date should normally be 1")

    for role in ("text", "image"):
        provider = str(nested(data, f"providers.{role}.type"))
        if provider not in PROVIDERS:
            warnings.append(f"providers.{role}.type is custom or unknown: {provider}")
        if provider not in {"none", "media-library", "local"}:
            block = nested(data, f"providers.{role}")
            if not block.get("secret_env") and not block.get("secret_file") and not block.get("secret_manager"):
                errors.append(f"providers.{role} must declare secret_env, secret_file, or secret_manager")

    image = nested(data, "providers.image")
    if image.get("type") not in {"none", "media-library"} and str(image.get("format", "")).lower() not in RASTER_FORMATS:
        errors.append("providers.image.format must be png, jpeg, jpg, or webp")

    publishing = nested(data, "publishing")
    mode = publishing.get("mode")
    if mode == "atomic-release":
        for field in ("root", "current_link", "releases_dir", "content_store", "cover_directory"):
            if not publishing.get(field):
                errors.append(f"publishing.{field} is required for atomic-release mode")
    elif mode not in {"cms-api", "database-transaction", "custom"}:
        errors.append("publishing.mode must be atomic-release, cms-api, database-transaction, or custom")

    safeguards = nested(data, "safeguards")
    for flag in ("atomic_activation", "rollback_on_live_failure", "preserve_previous_release"):
        if safeguards.get(flag) is not True:
            errors.append(f"safeguards.{flag} must be true")
    if nested(data, "providers.image.type") != "none" and safeguards.get("require_raster_cover") is not True:
        errors.append("safeguards.require_raster_cover must be true when images are enabled")

    errors.extend(find_plaintext_secrets(data))
    return errors, warnings

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.config.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: configuration not found: {args.config}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}", file=sys.stderr)
        return 2

    errors, warnings = validate(data)
    for item in warnings:
        print(f"WARNING: {item}")
    for item in errors:
        print(f"ERROR: {item}", file=sys.stderr)
    if errors:
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print("Configuration is valid and contains no obvious plaintext credentials.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

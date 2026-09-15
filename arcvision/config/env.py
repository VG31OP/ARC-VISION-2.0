import os
import re
from pathlib import Path
from typing import Annotated

from pydantic import AfterValidator, ValidationInfo

ARC_VISION_ENV_VARS: dict[str, str] = {}
FRIGATE_ENV_VARS = ARC_VISION_ENV_VARS  # Backward compatibility alias

for k, v in os.environ.items():
    if k.startswith("ARC_VISION_") or k.startswith("FRIGATE_"):
        ARC_VISION_ENV_VARS[k] = v

secrets_dir = os.environ.get("CREDENTIALS_DIRECTORY", "/run/secrets")
# read secret files as env vars too
if os.path.isdir(secrets_dir) and os.access(secrets_dir, os.R_OK):
    for secret_file in os.listdir(secrets_dir):
        if secret_file.startswith("ARC_VISION_") or secret_file.startswith("FRIGATE_"):
            ARC_VISION_ENV_VARS[secret_file] = (
                Path(os.path.join(secrets_dir, secret_file)).read_text().strip()
            )


# Matches an ARC_VISION_* or FRIGATE_* identifier following an opening brace.
_IDENT_RE = re.compile(r"(ARC_VISION_|FRIGATE_)[A-Za-z0-9_]+")
_FRIGATE_IDENT_RE = _IDENT_RE  # Backward compatibility alias


def _lookup_env_var(key: str) -> str:
    """Lookup variable with fallback between ARC_VISION_ and FRIGATE_."""
    if key in ARC_VISION_ENV_VARS:
        return ARC_VISION_ENV_VARS[key]
    if key.startswith("ARC_VISION_"):
        legacy_key = "FRIGATE_" + key[len("ARC_VISION_") :]
        if legacy_key in ARC_VISION_ENV_VARS:
            return ARC_VISION_ENV_VARS[legacy_key]
    elif key.startswith("FRIGATE_"):
        native_key = "ARC_VISION_" + key[len("FRIGATE_") :]
        if native_key in ARC_VISION_ENV_VARS:
            return ARC_VISION_ENV_VARS[native_key]
    raise KeyError(key)


def substitute_arcvision_vars(value: str) -> str:
    """Substitute `{ARC_VISION_*}` and `{FRIGATE_*}` placeholders in *value*.

    Reproduces the subset of `str.format()` brace semantics that config has
    historically supported, while leaving unrelated brace content untouched.
    """
    out: list[str] = []
    i = 0
    n = len(value)
    while i < n:
        ch = value[i]
        if ch == "{":
            # Escaped literal `{{`.
            if i + 1 < n and value[i + 1] == "{":
                out.append("{")
                i += 2
                continue
            # Possible `{ARC_VISION_*}` or `{FRIGATE_*}` placeholder.
            if value.startswith("{ARC_VISION_", i) or value.startswith("{FRIGATE_", i):
                ident_match = _IDENT_RE.match(value, i + 1)
                if (
                    ident_match is not None
                    and ident_match.end() < n
                    and value[ident_match.end()] == "}"
                ):
                    key = ident_match.group(0)
                    out.append(_lookup_env_var(key))
                    i = ident_match.end() + 1
                    continue
                # Looks like a variable placeholder but is malformed
                raise ValueError(
                    f"Malformed environment variable placeholder near {value[i : i + 32]!r}"
                )
            # Plain `{` — pass through.
            out.append("{")
            i += 1
            continue
        if ch == "}":
            # Escaped literal `}}`.
            if i + 1 < n and value[i + 1] == "}":
                out.append("}")
                i += 2
                continue
            out.append("}")
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


# Backward compatibility alias
substitute_frigate_vars = substitute_arcvision_vars


def validate_env_string(v: str) -> str:
    return substitute_arcvision_vars(v)


EnvString = Annotated[str, AfterValidator(validate_env_string)]


def validate_env_vars(v: dict[str, str], info: ValidationInfo) -> dict[str, str]:
    if isinstance(info.context, dict) and info.context.get("install", False):
        for k, val in v.items():
            os.environ[k] = val
            if k.startswith("ARC_VISION_") or k.startswith("FRIGATE_"):
                ARC_VISION_ENV_VARS[k] = val

    return v


EnvVars = Annotated[dict[str, str], AfterValidator(validate_env_vars)]

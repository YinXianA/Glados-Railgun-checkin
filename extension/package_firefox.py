"""Build the Firefox variant from the shared extension files."""

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def main() -> None:
    extension = Path(__file__).resolve().parent
    repository = extension.parent
    manifest = json.loads((extension / "manifest.json").read_text(encoding="utf-8"))
    manifest.pop("minimum_chrome_version")
    manifest["background"] = {"scripts": [manifest["background"]["service_worker"]]}
    manifest["browser_specific_settings"] = {
        "gecko": {
            "id": "glados-checkin@yin-xiana.github.io",
            "strict_min_version": "128.0",
        }
    }

    files = [
        "background.js",
        "inject.js",
        "options.css",
        "options.html",
        "options.js",
        "popup.css",
        "popup.html",
        "popup.js",
        *sorted(set(manifest["icons"].values())),
    ]
    entries = {name: (extension / name).read_bytes() for name in files}
    entries["LICENSE"] = (repository / "LICENSE").read_bytes()
    entries["manifest.json"] = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"

    output = repository / f"glados-checkin-extension-firefox-v{manifest['version']}.zip"
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for name, content in entries.items():
            archive.writestr(name, content)
    print(output)


if __name__ == "__main__":
    main()

# Parcel queue (synthetic)
Offline multi-tenant JSONL formatter; Python standard library only.
Run `python3 -m parcel input.jsonl [--tenant TENANT]`.
Run local tests: `python3 -m unittest discover -s tests -v`.
The CLI calls service.execute; loader and validation prepare records; selection
filters and deduplicates; render formats JSONL. Project discussions are in notes/.

Context entry point: [project context](docs/project-context.md).

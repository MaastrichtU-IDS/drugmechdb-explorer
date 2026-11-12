"""Build the DrugMechDB Pattern Explorer page.

Reads DrugMechDB's indication_paths.json, packs it into a compact JSON
document, and embeds it in the page template.

Usage: python build.py <indication_paths.json> <drugmechdb_commit> <out.html>
"""

import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).parent / "src" / "explorer.html"
PLACEHOLDER = "/*DATA*/"

# Node types in display order; the page refers to them by index.
TYPES = [
    "Drug", "ChemicalSubstance", "Protein", "GeneFamily", "MacromolecularComplex",
    "MolecularActivity", "BiologicalProcess", "CellularComponent", "Pathway", "Cell",
    "GrossAnatomicalStructure", "OrganismTaxon", "PhenotypicFeature", "Disease",
]


def pack(paths: list[dict], commit: str) -> dict:
    """Compact form: each mechanism is [id, drug, disease, drugbank, nodes, links, src, dst]."""
    type_index = {t: i for i, t in enumerate(TYPES)}
    unknown = sorted({n["label"] for g in paths for n in g["nodes"]} - type_index.keys())
    if unknown:
        sys.exit(f"Unknown node types in DrugMechDB (add them to TYPES and the page): {unknown}")
    preds = sorted({link["key"] for g in paths for link in g["links"]})
    pred_index = {p: i for i, p in enumerate(preds)}
    mechs, missing_endpoints = [], 0
    for g in paths:
        meta = g["graph"]
        index = {n["id"]: i for i, n in enumerate(g["nodes"])}
        drugbank = meta.get("drugbank") or ""
        src = index.get(meta["drug_mesh"], index.get(drugbank, -1))
        dst = index.get(meta["disease_mesh"], -1)
        missing_endpoints += src < 0 or dst < 0
        mechs.append([
            meta["_id"], meta["drug"], meta["disease"], drugbank.removeprefix("DB:"),
            [[n["id"], n["name"], type_index[n["label"]]] for n in g["nodes"]],
            [[index[l["source"]], pred_index[l["key"]], index[l["target"]]] for l in g["links"]],
            src, dst,
        ])
    print(f"{len(mechs)} mechanisms, {len(preds)} link labels, "
          f"{missing_endpoints} without a drug or disease endpoint", file=sys.stderr)
    return {"types": TYPES, "preds": preds, "mechs": mechs,
            "source": f"SuLab/DrugMechDB@{commit[:12]}"}


def main() -> None:
    paths_json, commit, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    data = json.dumps(pack(json.loads(Path(paths_json).read_text()), commit),
                      separators=(",", ":"), ensure_ascii=False)
    # The data sits inside a <script> element, so "</" must not appear verbatim.
    data = data.replace("</", "<\\/")
    template = TEMPLATE.read_text()
    if template.count(PLACEHOLDER) != 1:
        sys.exit(f"{TEMPLATE} must contain {PLACEHOLDER} exactly once")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(template.replace(PLACEHOLDER, data))
    print(f"wrote {out} ({out.stat().st_size / 1e6:.1f} MB)", file=sys.stderr)


if __name__ == "__main__":
    main()

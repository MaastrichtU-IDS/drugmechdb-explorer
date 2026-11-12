# DrugMechDB Pattern Explorer

A single-page tool to search and filter the curated drug mechanism graphs in [DrugMechDB](https://github.com/SuLab/DrugMechDB), and to see the node-type patterns they follow.

**Live page:** https://maastrichtu-ids.github.io/drugmechdb-explorer/

## What it shows

One set of filters drives four views, and every count and chart is recomputed for the mechanisms that match.

- **Filters:** free-text search (drug, disease, any entity name or identifier), scope (all, host only, or only node types that OptimusKG represents), shape (single chain or branched), a required link label, and node types to require or exclude.
- **Mechanisms:** the list, each mechanism drawn as a graph from drug to disease, its drug-to-disease routes, its links and its entities (with links to bioregistry.io).
- **Patterns:** route lengths, the first step after the drug and the last step before the disease, and the type sequences of routes (exact, or with repeated types merged). A mechanism with *k* routes gives each route weight 1/*k*.
- **Next-type transitions:** for each node type, the share of links that lead to each next type, with the link labels behind each cell.
- **Cardinality:** how many nodes of each type a mechanism has, how many next steps of each type follow a chosen type, and where mechanisms branch and merge.

## How it is built

`build.py` reads DrugMechDB's `indication_paths.json`, packs it into compact JSON and embeds it in `src/explorer.html`. The result is a single static page with no server or database.

The GitHub Actions workflow builds and deploys the page on every push to `main`, on the first of every month, and on demand. A manual run can name a DrugMechDB branch, tag or commit; otherwise it uses DrugMechDB's `main`. The page footer shows the DrugMechDB commit it was built from.

To build locally (Python 3.9 or later, no dependencies):

```sh
curl -fsSLO https://raw.githubusercontent.com/SuLab/DrugMechDB/main/indication_paths.json
python3 build.py indication_paths.json main site/index.html
python3 -m http.server -d site 8000
```

## Licences

The code is released under the MIT licence. DrugMechDB is released under [CC0 1.0](https://github.com/SuLab/DrugMechDB/blob/main/LICENSE); please cite it:

> Gonzalez-Cavazos AC, Tanska A, Mayers M, et al. DrugMechDB: A Curated Database of Drug Mechanisms. *Scientific Data* 10, 632 (2023). https://doi.org/10.1038/s41597-023-02534-z

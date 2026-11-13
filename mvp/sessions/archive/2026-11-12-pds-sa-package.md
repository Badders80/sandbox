# Session DoD — complete PDS/SA document package

**Status:** COMPLETE 2026-11-12 — local session gate green.

**Terminology:** as of 2026-11-13, the combined artifact is called the
**Investor Pack (PDS + SA)**. Historical gate language below is retained
unchanged.

## Outcome

One deterministic headless command produces one complete legal document package
from one checked-in sale fixture. It does not require the operator UI, Stripe,
KYC or a live database sale.

The package is a **synthetic sale** and both documents are visibly marked
`MOCK — NOT EXECUTED`. The document mechanics are real: the same compiler,
identifier rules, hashes, storage layout and manifest will be used for a real
sale.

Port `3001` is an optional visual check. It is not part of the completion gate.
The current `/dsl/[id]/legal` page only previews Markdown; it does not produce or
store the durable artefact.

## Input

One fixed fixture containing one horse, trainer, owner, DSL/listing, buyer,
stake and executed date, plus stable fixture UUIDs for `sale_id`, `dsl_id`,
`horse_id` and `account_id`.

The fixture is data, not production law. It may reuse Mulan The Brave and the
current Mulan draft terms once those fields are complete.

## Required identifiers

- `contract_id` is generated once before rendering and printed in both the PDS
  and SA. Format: `ES-DSL-YYYY-NNNNNN`.
- The same `contract_id` keys the local output directory and manifest.
- `sale_id`, `dsl_id`, `horse_id` and `account_id` are retained in the local
  provenance record so the document can be traced back to its source snapshot.
- The external-style manifest does not contain investor identity.

## Required hashes

- `pdf_sha256`: SHA-256 of the exact final combined PDF bytes.
- `pds_sha256`: SHA-256 of the exact rendered PDS Markdown.
- `sa_sha256`: SHA-256 of the exact rendered SA Markdown.
- `template_hashes`: the SHA-256 of each of the eight template/block files
  returned by the compiler.
- `legal_pack_version`: the compiler's printed pack version.

The source hashes prove what was compiled. The PDF hash proves the exact
durable artefact. Neither substitutes for the other.

## Local output

Write once to:

```text
/home/evo/sandbox/mvp/out/legal/<contract_id>/
```

The package contains:

- `contract.pdf` — one combined PDF, PDS first and SA second;
- `pds.md` — the exact rendered PDS source;
- `sa.md` — the exact rendered SA source;
- `manifest.json` — the six-field archive manifest;
- `provenance.json` — local source identifiers and source hashes;
- `SHA256SUMS` — at minimum the line for `contract.pdf`.

`manifest.json` contains exactly these top-level fields:

```json
{
  "contract_id": "ES-DSL-YYYY-NNNNNN",
  "sale_id": "fixture-uuid",
  "pdf_sha256": "64-lowercase-hex",
  "object_key": "out/legal/<contract_id>/contract.pdf",
  "template_versions": {
    "legal_pack": "1.0.2",
    "files": {}
  },
  "created_at": "RFC3339 UTC"
}
```

The write refuses to overwrite an existing contract directory. Re-running into
the same `contract_id` must fail until the operator chooses a new fixture
identity.

## Pass gate

All checks must run from the repository root with no browser open:

1. The command exits `0` and creates the complete directory above.
2. `pdfinfo contract.pdf` reports a valid PDF and at least two pages.
3. `pdftotext contract.pdf -` contains the contract ID at least twice, once in
   the PDS and once in the SA.
4. Extracted text contains `Product Disclosure Statement`, `Syndicate
   Agreement`, `Legal pack`, and `MOCK — NOT EXECUTED`.
5. `sha256sum contract.pdf` equals `manifest.pdf_sha256` and the PDF line in
   `SHA256SUMS`.
6. Recomputed hashes of `pds.md` and `sa.md` equal `provenance.json`.
7. Every file hash in `template_hashes` equals the current file on disk.
8. Re-reading the stored PDF produces the same hash; no recompilation is used to
   prove historical integrity.
9. A second compile of the fixture produces identical PDS/SA Markdown and source
   hashes. PDF-byte determinism is not required unless the PDF renderer can
   suppress volatile metadata.
10. The output contains no `{{` or `}}` tokens and no investor data in
    `manifest.json`.

## Not in this session

- Stripe, checkout, KYC or a real sale row.
- Email delivery.
- MyStable display.
- Cloud or WORM archive.
- Legal approval or current Rules of Racing verification.
- Changes to the locked commercial model.

## Starting point at lock

Already present in
`/home/evo/evolution/engine_v2/website/engine/`:

- locked PDS/SA templates and eight hashed source files;
- deterministic `compileLegalPack`, returning rendered Markdown and per-file
  template hashes;
- legal pack version `1.0.2`;
- `/dsl/[id]/legal`, which previews both documents and their Markdown hashes;
- sale storage for separate PDS/SA Markdown and hashes.

Still missing for this DoD:

- `contract_id` generation, database field and template token;
- combined PDF rendering;
- local write-once storage;
- exact-PDF-byte hashing;
- the six-field manifest and local provenance record;
- a headless command and gate covering the checks above.

## Implementation evidence

Implemented in `/home/evo/evolution/engine_v2/website`:

- `engine/src/lib/legal/package.ts` builds the write-once package, manifest,
  provenance and SHA-256 evidence.
- `engine/scripts/legal-package.ts` loads either the checked-in fixture or the
  saved Supabase DSL/horse/trainer/owner records.
- `engine/scripts/render-legal-pdf.py` renders the combined PDS/SA PDF
  headlessly with ReportLab (`engine/requirements-legal.txt`).
- `scripts/legal-package-dod.sh` runs the fixture gate.
- `scripts/verify-legal-package.sh` proves identifiers, hashes, template
  versions, PDF pages and extracted document text.
- `.github/workflows/ci.yml` installs ReportLab + Poppler and runs the DOD after
  `pnpm verify`.

Verification on 2026-11-12:

```text
pnpm verify
exit 0

engine tests
401 passed, 1 skipped

bash scripts/legal-package-dod.sh
PASS legal package ES-DSL-2026-900001
pages 10
```

Saved-record proof using the current Mulan DSL:

```text
DSL      5a46be50-41be-4fca-a554-793d5f1562fa
contract ES-DSL-2026-900006
PDF      /home/evo/sandbox/mvp/out/legal/ES-DSL-2026-900006/contract.pdf
pages    11
PASS     legal package ES-DSL-2026-900006
```

The extracted PDF text contains Mulan The Brave, Stephen Gray & Bridget Gray,
$65.00 per 1% per month, 75% investor return, quarterly distributions and the
30 Jun 2028 expiry.

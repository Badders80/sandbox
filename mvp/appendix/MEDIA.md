# Media — the speculative layer

Written 2026-11-11. Speculative, but constrained by the same rules as the rest:
one authority, evidence over assertion, no rule in a surface.

Scope: horse imagery, brand assets, race and stable content, and the rendered
document itself. Post-sale content is the bulk of it; the document artefact is
the part that matters most.

## 1. The classification is the design

Today everything is "images" with a count. That is why a placeholder, a hero
shot and a poster all behave the same way. Three classes, three rule sets:

| Class | Examples | Mutable? | Authority |
|---|---|---|---|
| **Evidence** | identity photos, microchip, registry documents, conformation | No — append only | The horse record |
| **Editorial** | hero image, card image, gallery slots | Replaceable, versioned | The horse record |
| **Derived** | posters, social cuts, video, rendered PDFs | Disposable, regenerable | Its provenance |

The rule that follows: **derived assets are never the source of truth.** A
poster can always be rebuilt from its source media, template version and brand
tokens. An evidence photo can never be rebuilt from anything.

## 2. Content addressing, not folder addressing

Storage keys are content hashes, not names.

```
media/<sha256>/<original-name>
manifest: sha256, mime, bytes, width, height, source, rights, created_by
```

Why it matters here specifically: the current R2 layout is keyed by horse name,
and a rename does not move the folder — a known defect. Content addressing makes
rename a database operation with zero storage work, and makes duplicate uploads
free.

Also: one store, one manifest. The duplicated `coming-soon.jpg` in `engine/` and
`website/` is the miniature version of the problem — two copies, no binding.

## 3. The document is a rendered artefact

Today the sale freezes `pds_markdown` and hashes it. The investor does not
receive markdown. They receive a rendered PDF.

**A hash over the source does not bind the artefact.** Change a font, a CSS
rule, a page break or a Chromium version and the same markdown renders a
different document. If the claim is "the executed document is frozen", the hash
must cover what was executed.

Design:

- Compile markdown → HTML → PDF at sale, inside the sale transaction's outbox.
- Hash the **PDF**, store `pdf_hash` alongside `pds_hash` / `sa_hash`.
- Archive the PDF, not only the markdown.
- Record renderer version and template version in the snapshot.

This is the single highest-value idea in this document, and it belongs in F3.

## 4. Rendering is a queue, not a request

Studio already does the right thing structurally: inputs → deterministic
outputs, HTML/CSS compositing, text never inside a diffusion model. Make it
stateless and asynchronous.

- Rendering never happens inside a page request or a webhook.
- A `render_jobs` row is written in the same transaction as the thing that needs
  the render; a worker drains it.
- Failure is visible: a job that dies leaves a row, not a silent blank tile.

## 5. Provenance

Every derived asset records what made it:

```
source_media_ids[], template, template_version, tokens_version, renderer_version, rendered_at
```

Then a brand change is a re-render, not a hunt. And a published poster can be
traced to the exact source image and the exact token set that produced it —
which is what you want if a marketing claim is ever questioned.

## 6. Rights and approval

Anything on a public surface carries two facts: who owns it, and who approved it.

- `rights`: owner, licence, expiry, territory.
- `approval`: approved_by, approved_at.
- A public page refuses an asset without both.

Two hard rules specific to this business:

1. **No AI-generated imagery of a horse presented as that horse.** Backgrounds,
   textures, layouts — fine. A generated horse standing in for Mulan on a page
   selling an interest in Mulan is a misrepresentation.
2. **No generated text in an image.** Already a studio rule; it becomes a rule
   in the register, not a habit.

## 7. Retirement, not deletion

Media follows the sales rule: `retired_at`, never `DELETE`. A published page
must be reconstructable, which means the asset that was on it must still exist.

This also answers the placeholder question honestly: a placeholder is a retired
slot with a known asset, not a missing row.

## 8. Studio's place

Studio stays a CLI with its own gate. It never writes the product.

The integration is one boundary: `studio/out/` → promote slot → media manifest →
linked to a horse. "Promote is a slot" is already the estate rule; this makes it
a state machine — `draft → approved → published` — with the same discipline as a
listing.

## 9. Post-sale content

The owner relationship continues after the sale. Keep it to three update kinds,
each tied to the horse and dated:

- race: entry, result, replay
- stable: spelling, training, travel
- veterinary: anything the owner should know

These are editorial, not evidence. They are also the raw material for the
monthly investor update, which is where media earns its keep commercially.

## 10. What not to build

- A CMS. The horse record is the CMS.
- A digital asset manager. The manifest is the DAM.
- A social scheduler.
- AI video at scale. One good clip beats ten generated ones, and the legal
  exposure is asymmetric.

## 11. Order

Nothing here precedes the DoD. If any of it is built early, build only this:

1. **PDF artefact + hash** — part of F3, because it changes what "frozen" means.
2. **Content addressing + manifest** — removes the rename defect permanently.
3. **Provenance on derived assets** — cheap once the manifest exists.
4. **The rest** — after the first real sale.

## 12. Failure modes this is designed against

| Failure | Today | With this |
|---|---|---|
| Rename breaks every image | Known defect | Hash keys, rename is a DB update |
| Same asset, two copies | `coming-soon.jpg` ×2 | One store, one manifest |
| Frozen document re-renders differently | Hash covers markdown only | Hash covers the PDF |
| Poster out of date after a brand change | Manual hunt | Provenance + re-render |
| Unlicensed or generated horse image published | No record | Rights + approval gate |
| Deleted image, unreconstructable page | Possible | Retirement only |

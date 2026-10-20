"""Reproduce batch-one manual coding, checking excerpts against the frozen release.

This is a single-coder evidence transcription, not a semantic labeler. The hand
assignments are functions below. Full source text is never written to outputs.
"""

import csv
import hashlib
import json
from collections import Counter, defaultdict
from profile import ROOT, SLUGS, profile, records

from film_practice import TABLES, connect

VERSION = "1.0"
UNKNOWN = {
    "02.1": (
        "No substantive technical brief intent is disclosed; "
        "catalogue synopsis does not supply a production plan."
    ),
    "02.2": (
        "No persistent planned entity can be established from the "
        "inspected instructions."
    ),
    "02.3": (
        "No explicit scene/shot plan is established by the inspected "
        "text; a single shot request is not a shot list."
    ),
    "02.4": (
        "No independently identifiable plan entity/task match is "
        "established; folder and name resemblance alone is "
        "insufficient."
    ),
    "02.5": (
        "No preparation sequence is established as the project build "
        "order; dates and folders cannot settle it."
    ),
    "02.6": (
        "Brief is unavailable, so template versus substantive "
        "sections cannot be classified."
    ),
    "03.1": (
        "No reusable entity category is established in the inspected "
        "instructions or disclosed reference metadata."
    ),
    "03.2": (
        "No explicit same-identity or named-variant instruction is "
        "established in inspected records."
    ),
    "03.3": (
        "No disclosed reference package or package-creation request "
        "is established in inspected records."
    ),
    "03.4": ("Property storage cannot be assigned from the inspected fields."),
    "03.5": (
        "No named element-version linkage with changed properties is "
        "established; distinct outputs are not automatically "
        "versions."
    ),
    "03.6": (
        "No explicit scoped canonical declaration or alias-audited "
        "reuse hub is established in inspected records."
    ),
    "04.1": "Text role cannot be resolved from the exported source paths.",
    "04.2": ("Inspected text does not decide semantic instruction components."),
    "04.3": (
        "No input usages are exported; text-only operation cannot be "
        "established from missing attachments."
    ),
    "04.4": (
        "Attached media content is unobservable; no properties can be assigned to it."
    ),
    "04.5": "Prompt structure is unresolved in inspected text.",
    "04.6": (
        "No sufficiently scoped conflicting pair is established in "
        "inspected text; this is not a film-wide absence."
    ),
    "05.1": "Image operation is unresolved in inspected records.",
    "05.2": (
        "No multi-input or staged image construction is established by inspected edges."
    ),
    "05.3": (
        "No linked integration/preservation instruction is "
        "established in inspected image records."
    ),
    "05.4": (
        "No disclosed mechanism is established; language alone is not a mask or layer."
    ),
    "05.5": (
        "No explicit still-purpose declaration is established for inspected images."
    ),
    "06.1": "No video route is established in inspected records.",
    "06.2": "Motion intent is unresolved in inspected video text.",
    "06.3": (
        "No ordered/timed events or shot boundaries are established "
        "in inspected video text."
    ),
    "06.4": "Audio intent is unresolved in inspected video records.",
    "06.5": ("No explicit invariant is established in inspected video instructions."),
    "06.6": "Literal video controls are unresolved in inspected records.",
    "06.7": (
        "No changed video instruction with a scoped revision request "
        "is established in inspected records."
    ),
    "07.1": ("Producer/input relationships are unresolved in inspected records."),
    "07.2": ("No alias-audited structural motif is established in inspected edges."),
    "07.3": (
        "Variant metadata does not establish asset equivalence in the inspected scope."
    ),
    "07.4": (
        "No shared-input or output-chaining strategy is established by inspected edges."
    ),
    "07.5": (
        "No bounded changed-input descendant set has been enumerated in this case file."
    ),
    "08.1": ("Operation role is not established from literal model names alone."),
    "08.2": "Literal model identifier is unavailable.",
    "08.3": "Cross-model transition is unresolved in inspected edges.",
    "08.4": (
        "A supported workflow shape is unresolved; missing inputs do "
        "not prove a direct route."
    ),
    "08.5": (
        "No audio/finishing job or explicit external-tool statement "
        "is established; sound intent is not an audio job."
    ),
    "09.1": (
        "No multi-member batch/input/lineage family is established "
        "in inspected records; singleton batches do not suffice."
    ),
    "09.2": (
        "No iteration mode is established for a supported family or "
        "explicit correction request."
    ),
    "09.3": (
        "No directional revision delta is established between named "
        "family members; equality or co-membership does not "
        "establish revision order."
    ),
    "09.4": (
        "No later consumer or explicit approval is established for "
        "inspected outputs; this does not imply rejection."
    ),
}


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


class Case:
    def __init__(self, db, panel, codebook):
        self.db, self.panel, self.codebook = db, panel, codebook
        self.fid, self.title = panel["film_id"], panel["title"]
        self.slug = SLUGS[self.title]
        self.tables = {t: records(db, t, self.fid) for t in TABLES}
        self.jobs = {g["generation_id"]: g for g in self.tables["generations"]}
        self.n = len(self.jobs)
        self.reading = json.loads((ROOT / self.slug / "profile.json").read_text())
        self.selected = {r["generation_id"] for r in self.reading["reading_register"]}
        self.rows = {}
        self.audit = []
        self.base = self.aggregate(
            "generations; all 14 tables profiled by case-files/profile.py",
            f"{self.n} exported jobs; "
            f"{len(self.selected)} jobs selected for technical reading",
            f"One registered primary film; {self.n} jobs; "
            f"{len(self.selected)} inspected jobs",
        )
        for c in codebook:
            code = c["code_id"]
            if code in UNKNOWN:
                self.assign(code, r"\N", self.base, UNKNOWN[code], status="unknown")

    def key(self, kind, ident):
        return f"{self.fid}/{kind}:{ident}"

    def aggregate(self, path, excerpt, denominator, entities=None):
        return dict(
            entity_ids=entities or self.key("film", self.fid),
            source_path=path,
            excerpt=excerpt,
            denominator=denominator,
        )

    def find(self, prefix):
        matches = [g for gid, g in self.jobs.items() if gid.startswith(prefix)]
        assert len(matches) == 1, prefix
        return matches[0]

    def job(self, prefix, *spans, controls=(), inputs=False):
        g = self.find(prefix)
        gid = g["generation_id"]
        assert gid in self.selected, "Evidence job must be in reading register"
        pieces = []
        for span in spans:
            assert span in (g["prompt"] or ""), (self.slug, gid, span)
            assert span != g["prompt"], "Do not reproduce complete prompts"
            pieces.append(span)
        obj = json.loads(g["parameters_json"])
        if controls:
            pieces.append(
                "[literal controls] "
                + json.dumps(
                    {k: obj[k] if k in obj else "<unavailable>" for k in controls},
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        pieces.append(
            "[literal model_identifier] "
            + g["model_identifier"]
            + " [literal model_name] "
            + str(g["model_name"])
        )
        entities = [self.key("generation", gid)]
        path = "generations.prompt/model_identifier/model_name"
        if controls:
            path += "; generations.parameters_json." + "/".join(controls)
        if inputs:
            usage = [
                u
                for u in self.tables["asset_usages"]
                if u["generation_id"] == gid and u["asset_role"] != "output"
            ]
            entities += [self.key("asset", u["asset_id"]) for u in usage]
            entities += [
                self.key("reference", u["reference_element_id"])
                for u in usage
                if u["reference_element_id"]
            ]
            pieces.append(
                "[input usage role/path] "
                + json.dumps(
                    [
                        [
                            u["asset_id"],
                            u["asset_role"],
                            u["parameter_path"],
                            u["reference_element_id"],
                        ]
                        for u in sorted(
                            usage, key=lambda u: (u["asset_id"], u["parameter_path"])
                        )
                    ],
                    ensure_ascii=False,
                )
            )
            path += (
                "; asset_usages.asset_id/asset_role/parameter_path/reference_element_id"
            )
            refs = [
                r
                for r in self.tables["reference_elements"]
                if r["reference_element_id"]
                in {u["reference_element_id"] for u in usage}
            ]
            if refs:
                pieces.append(
                    "[disclosed reference metadata] "
                    + json.dumps(
                        [
                            {
                                k: r[k]
                                for k in ["reference_element_id", "name", "category"]
                            }
                            for r in refs
                        ],
                        ensure_ascii=False,
                        sort_keys=True,
                    )
                )
                path += "; reference_elements.reference_element_id/name/category"
        path += "; " + g["source_record_file"]
        return self.aggregate(
            path,
            " [excerpt boundary] ".join(pieces),
            f"One named job / {len(self.selected)} inspected / {self.n} exported jobs; "
            "input rows are occurrences, not independent evidence",
            "; ".join(dict.fromkeys(entities)),
        )

    def brief(self, span):
        text = self.tables["films"][0]["project_brief"]
        assert span in text and span != text
        return self.aggregate(
            "films.project_brief", span, "One visible brief section / one film"
        )

    def edge(self, producer, consumer):
        p, c = self.find(producer), self.find(consumer)
        matches = []
        assets = {a["asset_id"]: a for a in self.tables["assets"]}
        for u in self.tables["asset_usages"]:
            a = assets.get(u["asset_id"])
            if (
                u["generation_id"] == c["generation_id"]
                and u["asset_role"] != "output"
                and a
                and a["generation_id"] == p["generation_id"]
            ):
                matches.append(u)
        assert matches
        self.audit.append(
            {
                "producer": p["generation_id"],
                "consumer": c["generation_id"],
                "usages": [
                    {k: u[k] for k in ["asset_id", "asset_role", "parameter_path"]}
                    for u in matches
                ],
            }
        )
        return self.aggregate(
            "assets.generation_id/asset_id -> generations; "
            + ("asset_usages.generation_id/asset_id/asset_role/parameter_path"),
            f"[producer model] {p['model_identifier']} "
            f"[consumer model] {c['model_identifier']} "
            "[explicit usage] "
            + json.dumps(
                [
                    {k: u[k] for k in ["asset_id", "asset_role", "parameter_path"]}
                    for u in matches
                ],
                sort_keys=True,
            ),
            (
                "One named producer/consumer pair; exact asset IDs; all film "
                "assets/usages searched; "
            )
            + ("raw/min metadata variants retained under their one asset entity"),
            "; ".join(
                [
                    self.key("generation", p["generation_id"]),
                    self.key("generation", c["generation_id"]),
                ]
                + [self.key("asset", u["asset_id"]) for u in matches]
            ),
        )

    def family(self, prefixes):
        jobs = [self.find(p) for p in prefixes]
        sets = [
            {
                u["asset_id"]
                for u in self.tables["asset_usages"]
                if u["generation_id"] == g["generation_id"]
                and u["asset_role"] != "output"
            }
            for g in jobs
        ]
        common = set.intersection(*sets)
        assert common
        equal = len({g["prompt"] for g in jobs}) == 1
        return self.aggregate(
            "generations.prompt/generation_batch_id/model_identifier; "
            + ("asset_usages.asset_id/generation_id/asset_role; assets.metadata_json"),
            "[shared input IDs] "
            + ",".join(sorted(common))
            + f"; named family members={len(jobs)}; "
            f"exact primary text equality={equal}; "
            + "[models] "
            + ",".join(g["model_identifier"] for g in jobs),
            f"{len(jobs)} named family members / {self.n} jobs; "
            "candidate based on shared inputs; "
            + (
                "same asset IDs deduplicated within consumer; aliases not "
                "merged across IDs"
            ),
            "; ".join(
                [self.key("generation", g["generation_id"]) for g in jobs]
                + [self.key("asset", a) for a in sorted(common)]
            ),
        )

    def assign(
        self,
        code,
        value,
        evidence,
        note,
        status="coded",
        label="observed",
        alternative=None,
    ):
        definition = next(c for c in self.codebook if c["code_id"] == code)
        if status == "coded":
            assert set(value.split("|")) <= set(definition["values"].split("|")), (
                code,
                value,
            )
        self.rows[code] = dict(
            film_id=self.fid,
            title=self.title,
            population="primary",
            code_id=code,
            later_study=definition["study"],
            value=value,
            status=status,
            evidence_id=self.slug + ":" + code,
            scope_note=note,
            codebook_version=VERSION,
            study=definition["study"],
            **evidence,
            evidence_label=label,
            competing_explanation=alternative
            or (
                (
                    "Published histories can omit external/private work; "
                    "instructions do not establish "
                )
                + "achieved results, final acceptance or project-wide intent."
            ),
            confidence_rationale=(
                (
                    "Direct source paths/compound keys and exact excerpt or "
                    "deterministic aggregate checked "
                )
                + (
                    "during reproduction; single-coder semantic interpretation, "
                    "scoped to named evidence. "
                )
                + (
                    "Evidence does not decide this code; no absence inference."
                    if status == "unknown"
                    else "No agreement or quality estimate."
                )
            ),
        )

    def common(self, organisation):
        g = min(self.jobs.values(), key=lambda g: g["generation_id"])
        prefix = g["generation_id"]
        e = self.job(prefix)
        primary = [
            r
            for r in self.tables["generation_prompts"]
            if r["generation_id"] == prefix and r["field_path"] == "params.prompt"
        ]
        assert len(primary) == 1 and primary[0]["text"] == g["prompt"]
        e["source_path"] += "; generation_prompts.field_path/text"
        e["excerpt"] += " [primary crosswalk] params.prompt"
        self.assign(
            "04.1",
            "primary",
            e,
            (
                "One primary text field crosswalk; nested params.prompt is "
                "the same field, not a second prompt."
            ),
        )
        self.assign(
            "08.2",
            "literal_identifier",
            self.job(prefix),
            (
                "One named job; identifier and display name retained "
                "independently; no provider inference."
            ),
        )
        folders = sorted(self.tables["folders"], key=lambda r: r["folder_id"])
        e = self.aggregate(
            ("folders.folder_name/parent_folder_id; generation_folders.folder_id"),
            "; ".join(r["folder_name"] for r in folders),
            f"{len(folders)} folder entities; "
            f"{len(self.tables['generation_folders'])} generation placements / "
            f"{self.n} jobs",
            "; ".join(self.key("folder", r["folder_id"]) for r in folders),
        )
        self.assign(
            "10.1",
            organisation,
            e,
            (
                "Literal organisation labels; their semantic grouping is "
                "inferred, not executed order."
            ),
            label="inferred",
        )
        authors = sorted(
            {g["author_user_id"] for g in self.jobs.values() if g["author_user_id"]}
        )
        covered = sum(bool(g["author_user_id"]) for g in self.jobs.values())
        self.assign(
            "10.2",
            "single_recorded_author"
            if len(authors) == 1
            else "multiple_recorded_authors",
            self.aggregate(
                "generations.author_user_id",
                json.dumps(authors),
                f"{covered}/{self.n} jobs with author ID; {len(authors)} distinct IDs",
                "; ".join(self.key("author", a) for a in authors),
            ),
            (
                "Recorded author IDs only; no employment, labour division or "
                "team inference."
            ),
        )
        events = self.db.execute(
            "SELECT count(try_cast(created_at AS TIMESTAMPTZ)), "
            "cast(min(try_cast(created_at AS TIMESTAMPTZ)) AS VARCHAR), "
            "cast(max(try_cast(created_at AS TIMESTAMPTZ)) AS VARCHAR) "
            "FROM generations WHERE film_id=?",
            [self.fid],
        ).fetchone()
        self.assign(
            "10.3",
            "recorded_event_window",
            self.aggregate(
                "generations.created_at",
                json.dumps(events),
                f"{events[0]}/{self.n} parseable recorded timestamps",
            ),
            (
                "UTC event extrema only; not labour time, latency or "
                "production duration."
            ),
        )
        duration = self.tables["films"][0]["duration"]
        ratio = self.n / float(duration) * 60
        self.assign(
            "10.5",
            "jobs_per_declared_minute",
            self.aggregate(
                "films.duration; generations.generation_id",
                f"recorded_jobs={self.n}; catalogue_duration_seconds={duration}; "
                f"jobs_per_declared_minute={ratio:.6f}",
                f"{self.n} recorded jobs / "
                f"({duration} catalogue-declared seconds / 60)",
            ),
            (
                "Descriptive proxy within this film only; brief-declared "
                "format is separate; no productivity or cost comparison."
            ),
        )
        texts = [g["prompt"] for g in self.jobs.values() if g["prompt"]]
        repeated = len(texts) - len(set(texts))
        multi = self.db.execute(
            ("SELECT count(*) FROM (SELECT generation_id FROM generation_folders ")
            + ("WHERE film_id=? GROUP BY 1 HAVING count(DISTINCT folder_id)>1)"),
            [self.fid],
        ).fetchone()[0]
        vals = []
        if repeated:
            vals.append("repeated_prompt")
        if multi:
            vals.append("multiple_folder_placements")
        e = self.aggregate(
            ("generations.prompt; generation_folders.generation_id/folder_id"),
            f"nonempty={len(texts)}; distinct_nonempty={len(set(texts))}; "
            f"repeat_occurrences_beyond_first={repeated}; "
            f"jobs_in_multiple_folders={multi}",
            f"{self.n} jobs; {len(texts)} nonempty primary fields; "
            f"{len(self.tables['generation_folders'])} placement rows",
        )
        self.assign(
            "10.4",
            "|".join(vals) if vals else r"\N",
            e,
            (
                "Exact primary text equality; placements counted separately; "
                "no waste/efficiency inference."
            ),
            status="coded" if vals else "not_observed_in_scope",
        )
        # Raw/min are explicitly grouped inside one metadata object: a scoped
        # variant example, not a claim that all cross-ID aliases are resolved.
        variants = []
        for a in sorted(self.tables["assets"], key=lambda a: a["asset_id"]):
            try:
                obj = json.loads(a["metadata_json"])
            except (TypeError, ValueError):
                continue
            if isinstance(obj, dict) and obj.get("raw") and obj.get("min"):
                variants.append((a, obj))
        if variants:
            a, obj = variants[0]
            self.assign(
                "07.3",
                "explicit_variant",
                self.aggregate(
                    "assets.asset_id/metadata_json.raw/min",
                    "[metadata keys] raw; min; [raw type] "
                    + str(obj["raw"].get("type"))
                    + "; [min type] "
                    + str(obj["min"].get("type")),
                    (
                        "One asset entity with explicitly grouped raw/min "
                        "representations; no cross-ID merging"
                    ),
                    self.key("asset", a["asset_id"]),
                ),
                (
                    "Metadata association only; not visual identity "
                    "verification. Cross-ID variants remain unresolved."
                ),
            )
        if self.tables["films"][0]["project_brief"] is None:
            e = self.aggregate(
                "films.project_brief",
                "[unavailable/null]",
                "One unavailable brief / one film",
            )
            for c in ["02.1", "02.6"]:
                self.assign(c, r"\N", e, UNKNOWN[c], status="unknown")

    def descendants(self, root):
        gid = self.find(root)["generation_id"]
        assets = {a["asset_id"]: a for a in self.tables["assets"]}
        adjacency = defaultdict(set)
        for u in self.tables["asset_usages"]:
            a = assets.get(u["asset_id"])
            if u["asset_role"] != "output" and a and a["generation_id"] in self.jobs:
                adjacency[a["generation_id"]].add(u["generation_id"])
        seen = set()
        todo = list(adjacency[gid])
        while todo:
            child = todo.pop()
            if child in seen:
                continue
            seen.add(child)
            todo.extend(adjacency[child] - seen)
        seen.discard(gid)
        assert seen
        # Preserve every explicit edge in the bounded traced example as well as
        # its descendant set; deduplicate the ledger in write().
        for producer in sorted({gid} | seen):
            for consumer in sorted(adjacency[producer] & seen):
                self.edge(producer, consumer)
        self.assign(
            "07.5",
            "reachable_dependency_set",
            self.aggregate(
                (
                    "assets.generation_id; asset_usages.asset_id/generation_id; "
                    "case-files/build.py:descendants"
                ),
                "[root generation] "
                + gid
                + "; [reachable generation IDs] "
                + ",".join(sorted(seen)),
                f"{len(seen)} reachable generation nodes from one named producer; "
                f"all {self.n} jobs and all film usages/assets searched; "
                "exact IDs only",
                "; ".join(self.key("generation", g) for g in [gid, *sorted(seen)]),
            ),
            (
                "Proposed review set after a root output change; observed "
                "reachability does not prove visual impact. "
            )
            + (
                "Excludes omitted/private edges and does not collapse cross-ID aliases."
            ),
            label="proposed",
        )

    def write(self):
        assert self.rows.keys() == {c["code_id"] for c in self.codebook}
        dest = ROOT / self.slug
        columns = list(
            csv.DictReader(
                (ROOT.parent / "studies/01-corpus/outputs/calibration.csv").open()
            ).fieldnames
        )
        with (dest / "codes.csv").open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
            writer.writeheader()
            writer.writerows(self.rows[c["code_id"]] for c in self.codebook)
        audit = []
        for edge in self.audit:
            if edge not in audit:
                audit.append(edge)
        dump(dest / "traced-edges.json", {"film_id": self.fid, "edges": audit})
        print(self.title, dict(Counter(r["status"] for r in self.rows.values())))


def dry(c):
    c.common("flat_proxy")
    image = c.job("3e7791d1", "FOREGROUND:", "MIDDLE GROUND:", "BACKGROUND:")
    c.assign(
        "03.4",
        "prose",
        image,
        (
            "Spatial properties are written in the image request; no "
            "media properties inferred."
        ),
    )
    c.assign(
        "04.2",
        "environment|composition",
        image,
        "Named depth-plane sections in one image request.",
    )
    c.assign(
        "04.4",
        "text_explicit",
        image,
        ("Foreground/middle/background are text-explicit; no input usage is exported."),
    )
    c.assign(
        "04.5",
        "sectioned|full_description",
        image,
        (
            "One sectioned environmental still request, not a quality or "
            "overload judgement."
        ),
    )
    c.assign(
        "05.1",
        "fresh_candidate",
        c.job(
            "3e7791d1",
            "No people, no animals.",
            controls=("input_images", "input_image"),
            inputs=True,
        ),
        (
            "One image job with empty input_images and null input_image; "
            "only a fresh candidate, not proven text-only."
        ),
    )
    c.assign(
        "05.4",
        "unspecified",
        image,
        (
            "No disclosed mask/layer/inpaint mechanism in this image "
            "job; operation mechanism unspecified."
        ),
    )
    c.assign(
        "08.1",
        "environment",
        image,
        ("Explicit environment construction instructions in one nano_banana_2 job."),
    )
    video = c.job(
        "c32600a6",
        "slow push-in",
        "SFX only.",
        controls=(
            "duration",
            "aspect_ratio",
            "resolution",
            "generate_audio",
            "multi_shots",
            "draft",
            "extension_mode",
        ),
        inputs=True,
    )
    c.assign(
        "06.1",
        "text_candidate",
        video,
        ("One video job with no exported input usages; text candidate only."),
    )
    c.assign(
        "06.2",
        "camera_action",
        video,
        ("Explicit push-in instruction; motion achieved is not observed."),
    )
    c.assign(
        "06.4",
        "ambience|generate_audio_true",
        video,
        (
            "SFX-only instruction and enabled audio flag; no standalone "
            "audio jobs inferred."
        ),
    )
    c.assign(
        "06.6",
        "duration|aspect_ratio|resolution|draft|extension",
        video,
        (
            "Raw Seedance values retained, including false draft and "
            "null extension_mode."
        ),
    )
    models = c.aggregate(
        ("generations.model_identifier; assets.generation_id; asset_usages.asset_role"),
        ("nano_banana_2: 1; seedance_2_5: 10; exported non-output usages: 0"),
        ("All 11 jobs; all 11 usage rows and 17 asset entities searched"),
    )
    c.assign(
        "08.3",
        "cooccurrence_only",
        models,
        ("Two literal models co-occur; no producer/input transition is exposed."),
    )
    c.assign(
        "07.1",
        r"\N",
        models,
        (
            "Only output usages are exported; no dependency input is "
            "available for this code."
        ),
        status="unknown",
    )


def titanic(c):
    c.common("flat_proxy")
    image = c.job(
        "416eb299",
        "make a character sheet.",
        ("Generate face close-up, side profil view, rear profil, and full body."),
        "Subject <<<image_1>>>:",
        "Wardrobe <<<image_2>>>: He wearing worn brown waistcoat,",
        inputs=True,
    )
    for code, value, note in [
        (
            "02.2",
            "character",
            (
                "Persistent character sheet is explicitly requested; no "
                "narrative reconstruction."
            ),
        ),
        (
            "03.1",
            "character|outfit",
            (
                "Subject and wardrobe are specified in the sheet request; no "
                "named element metadata exported."
            ),
        ),
        (
            "03.3",
            "multi_angle",
            ("Multi-angle sheet is requested; no claim that output fulfils it."),
        ),
        (
            "03.4",
            "prose",
            (
                "Character and wardrobe properties are written in text; "
                "attached content remains unobservable."
            ),
        ),
        (
            "04.2",
            "subject|identity",
            ("Subject description and wardrobe binding in one image request."),
        ),
        (
            "04.3",
            "media_input",
            (
                "Two actual input_asset usages; tokens are paired by "
                "parameter position, not media inspection."
            ),
        ),
        (
            "04.4",
            "text_explicit|media_attached_content_unknown",
            "Text specifies subject/wardrobe; media content is unknown.",
        ),
        (
            "04.5",
            "sectioned|reference_tokens",
            ("Subject/Grooming/Wardrobe/location sections and numbered image tokens."),
        ),
        (
            "05.1",
            "reference_guided|multi_input",
            (
                "Two disclosed input asset IDs condition one image request; "
                "no layers inferred."
            ),
        ),
        (
            "05.2",
            "multiple_inputs",
            (
                "Two input_asset occurrences with two distinct IDs; no "
                "compositing-layer claim."
            ),
        ),
        (
            "05.5",
            "reference_sheet",
            ("Explicit sheet request; output fulfilment cannot be assessed."),
        ),
        (
            "08.1",
            "reference_sheet",
            ("nano_banana_2 is used for a sheet request, not a verified sheet output."),
        ),
        (
            "07.1",
            "generation_input|external_or_unresolved",
            ("Two input IDs have no resolved producer among this film’s four jobs."),
        ),
    ]:
        c.assign(code, value, image, note)
    c.assign(
        "05.4",
        "unspecified",
        c.job("416eb299", controls=("input_image", "application", "surface")),
        (
            "Null fields retained; no nonempty mask/layer or explicit "
            "inpaint boolean disclosed."
        ),
    )
    family = c.family(["416eb299", "6e4ad139", "7277e1f4", "a1d84f68"])
    c.assign(
        "07.2",
        "shared_ancestor|branch",
        family,
        (
            "Scoped bipartite motif: each of two exact input IDs "
            "connects to the four named consumers; no producer inferred."
        ),
    )
    c.assign(
        "07.4",
        "shared_reference",
        family,
        ("Same two input IDs reused across four requests; not canonical approval."),
    )
    c.assign(
        "08.4",
        "branching",
        family,
        (
            "Branching at the disclosed inputs; upstream producers "
            "outside the observed four jobs are unresolved."
        ),
    )
    c.assign(
        "09.1",
        "shared_inputs",
        family,
        (
            "Four-member candidate family; all inputs and primary texts "
            "equal, four distinct batches."
        ),
    )
    c.assign(
        "09.2",
        "rerun",
        family,
        (
            "Repeated request observed: same literal model, primary text "
            "and two inputs; no success/failure interpretation."
        ),
        label="inferred",
    )
    c.assign(
        "09.3",
        r"\N",
        family,
        (
            "Exact primary text and inputs are unchanged within these "
            "four named requests; no delta in these compared fields."
        ),
        status="not_observed_in_scope",
    )
    scope = c.aggregate(
        "generations.generation_type/model_identifier",
        "image: 4; nano_banana_2: 4; video: 0",
        "All four exported generation records",
    )
    for code in [f"06.{i}" for i in range(1, 8)]:
        c.assign(
            code,
            r"\N",
            scope,
            (
                "No exported video jobs (0/4); video-job coding does not "
                "apply to this history; the finished film may include "
                "unrecorded video work."
            ),
            status="not_applicable",
        )
    c.assign(
        "08.3",
        r"\N",
        scope,
        (
            "Only one literal model in all four jobs; a cross-model "
            "transition question is not applicable to this exported "
            "history."
        ),
        status="not_applicable",
    )


def staff(c):
    c.common("scene|entity")
    brief = c.brief(
        "Format: 18-minute episodic anime pilot (split into 8 core "
        "narrative sequences)."
    )
    c.assign(
        "02.1",
        "deliverable",
        brief,
        (
            "Substantive Production section specifies format; "
            "creator-stated, not verified."
        ),
        label="creator-stated",
    )
    c.assign(
        "02.6",
        "substantive",
        brief,
        (
            "Context, Production, Status, Resources and Notes contain "
            "project-specific prose; no generic placeholder establishes "
            "a plan."
        ),
        label="creator-stated",
    )
    c.assign(
        "02.2",
        "character",
        c.brief("Character Sheets (Al-Qahtani, Sadeq, Reema, Noura)"),
        (
            "Named persistent characters in Resources; sheet "
            "availability/output not independently verified."
        ),
        label="creator-stated",
    )
    video = c.job(
        "04b90dc8",
        "SHOT 1 (0–4s)",
        "HARD CUT TO SHOT 2 (4–7s)",
        controls=(
            "duration",
            "multi_shots",
            "generate_audio",
            "aspect_ratio",
            "resolution",
            "draft",
            "extension_mode",
        ),
        inputs=True,
    )
    c.assign(
        "02.3",
        "shot_list|multi_shot_instruction",
        video,
        (
            "Timed shot list in one video prompt; separate from false "
            "multi_shots control."
        ),
    )
    linked = c.job(
        "1d963033", "frame 1 same last frame from here <<<video_1>>>", inputs=True
    )
    c.assign(
        "02.4",
        "explicit_link",
        linked,
        (
            "Prompt explicitly binds first-frame task to video_1 and a "
            "disclosed input_video; linkage is local to this request."
        ),
    )
    refs = sorted(
        c.tables["reference_elements"], key=lambda r: r["reference_element_id"]
    )
    e = c.aggregate(
        "reference_elements.name/category",
        "; ".join(r["name"] + ": " + r["category"] for r in refs),
        (
            "All 23 disclosed reference element entities; semantic "
            "examples are character and prop"
        ),
        "; ".join(c.key("reference", r["reference_element_id"]) for r in refs),
    )
    c.assign(
        "03.1",
        "character|prop|location",
        e,
        (
            "Retain character, prop and literal "
            "environment/auto:environment categories; location "
            "interpretation is inferred."
        ),
        label="inferred",
    )
    image = c.job(
        "6d514bd2",
        "Neatly organized character model sheet,",
        "Clean layout with organized poses and expressions.",
        "a slight sinister smirk",
        "while maintaining the exact original identity and art style.",
        controls=("is_inpaint",),
        inputs=True,
    )
    for code, value, note in [
        (
            "03.2",
            "identity_constraint",
            ("Explicit original-identity preservation in a sheet-edit request."),
        ),
        (
            "03.3",
            "expression_sheet",
            ("Organized poses/expressions requested; no verified fulfilment."),
        ),
        (
            "03.4",
            "prose",
            (
                "Identity and art-style preservation are specified in prose; "
                "raw editing controls are recorded separately under 05.4."
            ),
        ),
        (
            "04.2",
            "identity|preservation",
            "Explicit identity preservation in one image task.",
        ),
        (
            "04.3",
            "media_input",
            "One attached input image; media properties not viewed.",
        ),
        (
            "04.4",
            "text_explicit|media_attached_content_unknown",
            (
                "Identity/art-style preservation explicit in text; attached "
                "content unknown."
            ),
        ),
        (
            "04.5",
            "full_description",
            "Single paragraph sheet-edit request; no quality assessment.",
        ),
        (
            "05.1",
            "reference_guided|local_edit_request",
            (
                "Change expression/aura while maintaining identity; observed "
                "request, not a successful edit."
            ),
        ),
        (
            "05.3",
            "preservation",
            ("Maintain exact original identity/art style in a linked image task."),
        ),
        (
            "05.4",
            "inpaint_false",
            (
                "Explicit false retained; edit wording does not establish "
                "mask-based operation."
            ),
        ),
        ("05.5", "reference_sheet", "Model sheet request, not output verification."),
        (
            "08.1",
            "reference_sheet|local_edit",
            ("seedream_v5_pro carries a reference-guided sheet-edit request."),
        ),
    ]:
        c.assign(code, value, image, note)
    canonical = c.job(
        "27e11480",
        "Each element is the final authority on how that thing looks",
        inputs=True,
    )
    c.assign(
        "03.6",
        "creator_declared",
        canonical,
        (
            "Authoritative references scoped to this one generation; no "
            "project-wide canonical approval."
        ),
    )
    conflict = c.job(
        "46e851da",
        "THIS CLIP HAS NO SPEECH IN IT.",
        "A man speaks in Japanese, alone, close on his face.",
    )
    c.assign(
        "04.6",
        "possible_conflict",
        conflict,
        (
            "Same primary text combines no-speech clip instruction and "
            "appended speech directions; appended text may be intended "
            "as a separate task."
        ),
        label="inferred",
        alternative=(
            "Appended voice directions may be separate drafting material "
            "rather than instructions intended for this silent clip."
        ),
    )
    c.assign(
        "06.1",
        "multi_shot_request",
        video,
        (
            "Shot boundaries are requested while multi_shots=false; text "
            "and controls have separate scopes."
        ),
    )
    c.assign(
        "06.2",
        "camera_action",
        c.job("04b90dc8", "handheld tilt down and in, about half a metre"),
        ("Explicit camera movement in a named shot, not achieved motion."),
    )
    c.assign(
        "06.3",
        "timed_event|shot_boundary",
        video,
        "Written 0–4s and 4–7s boundaries; not observed timing.",
    )
    c.assign(
        "06.4",
        "generate_audio_true",
        video,
        (
            "True audio control only; no standalone sound production or "
            "usable output inferred."
        ),
    )
    c.assign(
        "06.5",
        "appearance",
        c.job(
            "04b90dc8",
            (
                "keeps exactly the same length, grain, copper collars and "
                "blunt copper foot"
            ),
        ),
        ("Staff appearance invariant scoped to the clip; fulfilment unknown."),
    )
    c.assign(
        "06.6",
        "duration|aspect_ratio|resolution|draft|extension",
        video,
        ("Literal model controls; null extension and false draft retained."),
    )
    edge = c.edge("0e619b88", "1d963033")
    c.assign(
        "07.1",
        "producer_output|generation_input",
        edge,
        ("One resolved input_video edge within the film; no chronology-based lineage."),
    )
    c.assign(
        "07.4",
        "previous_output_chaining",
        edge,
        (
            "One prior output is explicitly consumed by a later recorded "
            "job; not final acceptance."
        ),
    )
    c.assign(
        "08.3",
        "cooccurrence_only",
        c.aggregate(
            ("generations.model_identifier; assets.generation_id; asset_usages"),
            (
                "seedream_v5_pro: 1; cinematic_studio_video_4_0: 6; "
                "seedance_2_5: 75; resolved producer/input pairs: 1 "
                "(seedance_2_5 -> seedance_2_5)"
            ),
            "All 82 jobs, 121 assets and 462 usages searched",
        ),
        (
            "Three models co-occur, but the only resolved producer/input "
            "edge stays within seedance_2_5."
        ),
    )
    c.assign(
        "08.4",
        "staged",
        edge,
        (
            "One output-to-input stage; does not establish overall film "
            "pipeline or scheduler."
        ),
    )
    c.assign(
        "09.4",
        "reused_for_further_work",
        edge,
        "Explicit reuse is adoption for further work only.",
    )
    family = c.family(["04b90dc8", "ec163001"])
    c.assign(
        "07.2",
        "shared_ancestor|branch",
        family,
        (
            "Four exact reference assets shared by the two named "
            "consumers; only this motif is asserted, no film-wide hub "
            "degree."
        ),
    )
    c.assign(
        "09.1",
        "shared_inputs",
        family,
        (
            "Two named requests with identical primary text and "
            "reference inputs; a candidate family, not independent "
            "trials."
        ),
    )
    c.assign(
        "09.2",
        "rerun",
        family,
        (
            "Same primary text, model and shared inputs; rerun "
            "interpretation provisional, no outcome judgement."
        ),
        label="inferred",
    )
    c.descendants("0e619b88")


def apeirophobia(c):
    c.common("mixed")
    planned = c.job("95372c46", "Create a head-to-toe full-body character", inputs=True)
    c.assign(
        "02.2",
        "character",
        planned,
        (
            "Persistent named character representation requested; "
            "project-wide plan unavailable."
        ),
    )
    c.assign(
        "03.1",
        "character",
        planned,
        (
            "char_sicko reference metadata category is character; token "
            "and actual reference usage retained."
        ),
    )
    c.assign(
        "03.3",
        "named_element",
        planned,
        (
            "One disclosed named element attached to this full-body "
            "reference request; no sheet fulfilment claim."
        ),
    )
    c.assign(
        "03.4",
        "prose|reference_metadata",
        planned,
        (
            "Prose specifies appearance; reference metadata names "
            "char_sicko. Media content unobservable."
        ),
    )
    image = c.job(
        "0376b202",
        "replace the tattoo from the original image",
        "dont change image <<<image_1>>> only the tattoo",
        inputs=True,
    )
    for code, value, note in [
        (
            "03.2",
            "identity_constraint",
            ("Keep image identity except a specifically requested tattoo replacement."),
        ),
        (
            "04.2",
            "preservation|action",
            ("Tattoo replacement plus keep-other-image instruction; output unknown."),
        ),
        (
            "04.3",
            "media_input",
            "Actual attached inputs paired with numbered image tokens.",
        ),
        (
            "04.4",
            "text_explicit|media_attached_content_unknown",
            (
                "Target edit/preservation explicit; media property contents "
                "unobservable."
            ),
        ),
        (
            "04.5",
            "short_edit|reference_tokens",
            (
                "Short local request with numbered references; source "
                "remains in release."
            ),
        ),
        (
            "05.1",
            "local_edit_request|multi_input",
            (
                "Local tattoo replacement requested with two image input "
                "IDs; no mask inference."
            ),
        ),
        (
            "05.2",
            "multiple_inputs",
            (
                "Two distinct input_asset IDs condition one requested edit; "
                "no layers inferred."
            ),
        ),
        (
            "05.3",
            "preservation",
            ("Preserve image_1 except tattoo; no observed integration outcome."),
        ),
        (
            "08.1",
            "local_edit",
            ("nano_banana_2 used for explicit local tattoo correction request."),
        ),
        (
            "09.2",
            "local_correction_request",
            (
                "Observed request only; no prior defect/failure or "
                "successful correction inferred."
            ),
        ),
    ]:
        c.assign(code, value, image, note)
    c.assign(
        "05.4",
        "inpaint_false",
        c.job(
            "01ece7aa", "Closer Side Composition Cover Prompt", controls=("is_inpaint",)
        ),
        (
            "seedream_v5_pro image request explicitly has "
            "is_inpaint=false; mechanism assignment scoped to this job, "
            "not tattoo edit."
        ),
    )
    c.assign(
        "05.5",
        "poster",
        c.job("02fb03d9", "Create a cinematic festival key art poster"),
        "Explicit poster intent in gpt_image_2; not verified output.",
    )
    shot = c.job(
        "230fc3df",
        "EXACTLY TWO SHOTS ONLY — ONE SINGLE CUT.",
        controls=(
            "multi_shots",
            "duration",
            "generate_audio",
            "aspect_ratio",
            "resolution",
            "draft",
            "extension_mode",
        ),
        inputs=True,
    )
    c.assign(
        "02.3",
        "multi_shot_instruction",
        shot,
        ("Two shots explicitly requested; false multi_shots is a separate control."),
    )
    c.assign(
        "02.4",
        "explicit_link",
        planned,
        (
            "Named char_sicko token binds the persistent character "
            "request to an explicit reference-element usage; local "
            "instruction-to-task link."
        ),
    )
    canonical = c.job(
        "4896743a",
        ("This single reference image is authoritative for the entire shot."),
        inputs=True,
    )
    c.assign(
        "03.6",
        "creator_declared",
        canonical,
        (
            "Only the named shot makes one reference authoritative; no "
            "global library approval."
        ),
    )
    c.assign(
        "06.1",
        "multi_shot_request|image_guided",
        shot,
        (
            "Actual image usages plus two-shot request; no inference of "
            "successful route or enabled multi-shot feature."
        ),
    )
    c.assign(
        "06.2",
        "camera_action",
        c.job("81512453", "Slow zoom in"),
        "Explicit camera action in one kling3_0 job.",
    )
    c.assign(
        "06.3",
        "timed_event",
        c.job("4896743a", "After exactly 2 seconds,"),
        "Written event timing, not measured video timing.",
    )
    c.assign(
        "06.4",
        "dialogue|generate_audio_true",
        c.job(
            "4896743a",
            "with precise lip sync to the supplied audio:",
            controls=("generate_audio",),
            inputs=True,
        ),
        (
            "Dialogue intent with actual input_audio; no claim of "
            "usable/generated sound."
        ),
    )
    c.assign(
        "06.5",
        "identity|layout|appearance",
        c.job(
            "4896743a",
            "Preserve exactly what is shown in the reference image:",
            "the man’s identity, face, hair, tattoos, white shirt, bench, framing,",
            (
                "Do not add, remove, redesign, relight, restage, or "
                "reinterpret anything."
            ),
        ),
        "Requested invariants in one shot; fulfilment unknown.",
    )
    c.assign(
        "06.6",
        "duration|aspect_ratio|resolution|draft|extension",
        shot,
        (
            "Literal Seedance settings retained including false and "
            "null; camera terms in prose are separate."
        ),
    )
    revision = c.job(
        "0168082c",
        "remove the belt from his pants/trousers.",
        "the camera angle is supposed to remain the same",
        controls=("model", "duration"),
        inputs=True,
    )
    c.assign(
        "06.7",
        "video_edit_request",
        revision,
        (
            "video_edit request is explicitly linked to video input; no "
            "successful revision inferred."
        ),
    )
    edge = c.edge("2141cb13", "0168082c")
    c.assign(
        "07.1",
        "producer_output|generation_input",
        edge,
        ("Explicit same-film producer/input-video edge; raw chronology not used."),
    )
    c.assign(
        "07.4",
        "previous_output_chaining",
        edge,
        ("Observed output reuse for a video edit, not canonical approval."),
    )
    c.assign(
        "09.4",
        "reused_for_further_work",
        edge,
        ("Input edge shows further work; approval/final use remains unknown."),
    )
    cross = c.edge("88160a68", "b6e44e77")
    c.assign(
        "08.3",
        "edge_supported",
        cross,
        (
            "seedance_2_5 output consumed by cinematic_video_editor; "
            "direct asset ID edge."
        ),
    )
    c.assign(
        "08.4",
        "cross_model|staged",
        cross,
        (
            "One explicitly linked transition; model roles/internal "
            "routing are not inferred from names."
        ),
    )
    c.assign(
        "08.5",
        "job_observed",
        c.job("b6e44e77", controls=("duration", "chain_preset_id"), inputs=True),
        (
            "Literal cinematic_video_editor job with input video; no "
            "evidence of the final master or successful finishing."
        ),
    )
    family = c.family(["01ece7aa", "0a8dca0d", "123d45e6"])
    c.assign(
        "07.2",
        "shared_ancestor|branch",
        family,
        (
            "Four exact inputs shared by the three named consumers; "
            "scoped branching motif; no film-wide hub degree claimed."
        ),
    )
    c.assign(
        "09.1",
        "shared_inputs",
        family,
        (
            "Three named requests with identical text and input IDs "
            "across two literal model identifiers; intent/order "
            "unresolved."
        ),
    )
    c.descendants("88160a68")


def main():
    with (ROOT.parent / "studies/01-corpus/outputs/panel.csv").open() as stream:
        panel = [r for r in csv.DictReader(stream) if r["batch"] == "1"]
    with (ROOT.parent / "studies/01-corpus/outputs/codebook.csv").open() as stream:
        codebook = list(csv.DictReader(stream))
    with connect("data") as db:
        db.execute("SET TimeZone='UTC'")
        for film in panel:
            profile(db, film)
            c = Case(db, film, codebook)
            {
                "Dry Aged Dreams": dry,
                "The Staff": staff,
                "A Tales Before Titanic Tragedy": titanic,
                "APEIROPHOBIA": apeirophobia,
            }[film["title"]](c)
            c.write()
    files = sorted(
        p
        for slug in SLUGS.values()
        for p in (ROOT / slug).iterdir()
        if p.suffix in {".csv", ".json"}
    )
    dump(
        ROOT / "reproduction.json",
        {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in files
        },
    )


if __name__ == "__main__":
    main()

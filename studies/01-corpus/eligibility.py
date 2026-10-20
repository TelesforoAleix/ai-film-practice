"""Study 02–11 evidence eligibility; no future study results are assumed."""

import pandas as pd

REQUIREMENTS = {
    "02": (
        (
            "Brief-based planning: nonempty brief; prompt/folder "
            "reconstruction: primary history"
        ),
        (
            "Brief substance and plan-to-task links need case files; "
            "build order cannot follow dates alone"
        ),
    ),
    "03": (
        "Primary history; disclosed elements for element-metadata subanalysis",
        (
            "Authenticated libraries, canonical approval and "
            "identity/version links may be missing"
        ),
    ),
    "04": (
        "Primary history; nonempty primary or nested text for text subanalysis",
        (
            "Provider defaults, hidden prompts and media content "
            "unavailable; semantic scale labels pending"
        ),
    ),
    "05": (
        "Primary history with image jobs",
        (
            "No media inspection; absent usages do not establish "
            "text-only; masks/layers may be undisclosed"
        ),
    ),
    "06": (
        "Primary history with video jobs",
        (
            "Actual clip quality, used portions and equivalence of model "
            "controls unavailable"
        ),
    ),
    "07": (
        "Primary history; explicit usage edges for traced subanalysis",
        (
            "External producers, alias resolution, private/offline "
            "dependencies and canonical declarations may be missing"
        ),
    ),
    "08": (
        "Primary history with literal model identifiers",
        (
            "Roles need case coding; scheduler, agents, external audio "
            "and final editing unobservable"
        ),
    ),
    "09": (
        (
            "Primary history; batch/input/lineage-supported families "
            "only for revision comparisons"
        ),
        (
            "Family reconstruction pending; discarded/external work, "
            "defects and final acceptance unavailable"
        ),
    ),
    "10": (
        (
            "Primary history; dates/authors/folders analysed at their "
            "own coverage; duration for jobs/minute"
        ),
        "Labour time, spend, rendering latency and team structure unavailable",
    ),
    "11": (
        (
            "All 186 for catalogue/cohort context; 157 primary for "
            "production comparisons"
        ),
        (
            "Winners not in release; future announced winners and "
            "Studies 02–10 measures are dependencies"
        ),
    ),
}


def eligibility(frame, out):
    rows = []
    for study, (rule, missing) in REQUIREMENTS.items():
        for row in frame.to_dict("records"):
            primary = row["population"] == "primary"
            eligible = primary
            if study in ("05", "06"):
                count = row["image_jobs" if study == "05" else "video_jobs"]
                eligible = primary and pd.notna(count) and count > 0
            rows.append(
                {
                    "study": study,
                    "film_id": row["film_id"],
                    "population": row["population"],
                    "cohort_group": row["cohort_group"],
                    "production_eligible": eligible,
                    "catalogue_eligible": study == "11"
                    and row["population"] != "supplemental",
                    "eligibility_rule": rule,
                    "missing_evidence": missing
                    + (
                        "; primary workspace excluded/unavailable"
                        if not primary and row["population"] != "supplemental"
                        else "; supplemental analysed separately"
                        if not primary
                        else ""
                    ),
                }
            )
    result = pd.DataFrame(rows)
    result.to_csv(out / "eligibility.csv", index=False)
    summary = (
        result.groupby("study")
        .agg(
            production_films=("production_eligible", "sum"),
            catalogue_films=("catalogue_eligible", "sum"),
        )
        .reset_index()
    )
    summary["primary_denominator"] = 157
    summary["priority_denominator"] = 186
    summary["missing_evidence"] = summary.study.map(
        {k: v[1] for k, v in REQUIREMENTS.items()}
    )
    summary.to_csv(out / "eligibility_summary.csv", index=False)

# Keys to 100 Apps

Research agent for the Composio AI Product Ops take-home: which of 100 apps can become agent toolkits, and what blocks the rest.
Open `site/index.html` for the case study. `site/data.json` and `site/data.csv` hold every row with evidence.

## Run
Python 3.11+ and curl. Steps 1 to 4 need no keys.

    python3 pipeline/make_apps.py                   # 1. the 100 apps
    python3 pipeline/pass0_baseline.py              # 2. rule-based baseline
    python3 pipeline/check_evidence.py data/pass2   # 3. reload every cited page, match the quote
    python3 pipeline/score.py; python3 pipeline/holdout.py; python3 pipeline/cross_composio.py   # 4. accuracy
    pip install anthropic                           # 5. LLM passes (ANTHROPIC_API_KEY or `ant auth login`)
    python3 run_agent.py research --ids 11,12
    python3 run_agent.py verify   --ids 11,12
    python3 pipeline/finalize.py && python3 pipeline/build_page.py   # 6. rebuild the page

`run_agent.py` writes to `data/live/` and never overwrites the published run. It compiles but has not been run: no API key was available when this was built.

## How the published run worked
Claude Code subagents (Sonnet research, Opus verify) ran `prompts/pass1_research.md` and `prompts/pass2_verify.md` against `prompts/schema.md`.
Pass 0 rules -> pass 1 research -> quote check -> pass 2 adversarial verify -> score, Composio cross-check, browser disputes -> `data/overrides.json`.

## Honesty notes
- Gold and holdout labels were read in a browser by the supervising AI, not by a person. `data/human_checks.csv` is the human queue: fill `status` (done), `result`, `checked_by`, then rebuild the page.
- Some pass 2 gains come from rules clarified after the gold was written. See the page.
- Pass 2 notes include short quoted snippets from vendor pages for machine checking.

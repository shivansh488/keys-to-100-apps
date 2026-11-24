# Keys to 100 Apps

Research agent for the Composio AI Product Ops take-home: which of 100 apps can become agent toolkits, and what blocks the rest.
Live case study: https://shivansh488.github.io/keys-to-100-apps/ (source: `docs/index.html`). `site/data.json` and `site/data.csv` hold every row with evidence.

## Run
Scripts (Python 3.11+ and curl, nothing to install):

    python3 pipeline/make_apps.py                   # the 100 apps
    python3 pipeline/pass0_baseline.py              # rule-based baseline
    python3 pipeline/check_evidence.py data/pass2   # reload every cited page, match the quote
    python3 pipeline/score.py; python3 pipeline/holdout.py; python3 pipeline/cross_composio.py   # accuracy
    python3 pipeline/finalize.py && python3 pipeline/build_page.py   # rebuild the page

Research agent: open this repo in Claude Code and ask, one category at a time:

    Follow prompts/pass1_research.md and prompts/schema.md for ids 11-20. Write to data/live/pass1/cat02.json.

Then, in a fresh session so it has not seen the first answers being written:

    Follow prompts/pass2_verify.md for ids 11-20, reading data/live/pass1/cat02.json. Write to data/live/pass2/cat02.json.

`data/live/` keeps new runs apart from the published ones.

## Honesty notes
- Gold and holdout labels were read in a browser by the supervising AI, not by a person. `data/human_checks.csv` is the human queue: fill `status` (done), `result`, `checked_by`, then rebuild the page.
- Some pass 2 gains come from rules clarified after the gold was written. See the page.
- Evidence entries include short quoted snippets from vendor pages for machine checking.

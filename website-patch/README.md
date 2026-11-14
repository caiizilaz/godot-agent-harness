# SPACE8 LABS local source patch

This directory records the 13 reviewed changes applied to the separate non-Git website checkout.
`changes.patch` contains only reviewed changes; `files/` retains new files. `manifest.json` pins preimages and outputs.
`python3 website-patch/apply.py /path/to/space8labs` checks without writing;
add `--apply` to apply. Already-applied files are accepted, concurrent edits are rejected.
Prior versions are backed up before writes. No deployment is performed.

The site’s concurrently updated CSS, UI JavaScript and Work layout were retained.
Only harness additions, derived filter counts, localized navigation/metadata and verification changed.
No new artwork/font asset was introduced. Build outputs remain in the website’s `dist/`.

The live website may continue evolving after this snapshot. A preimage rejection is intentional;
merge only the harness hunks into newer files instead of replacing those files.

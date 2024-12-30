# Convert an array of {id, filename, url} entries into a Markdown-formatted report
[
    "### Attestations Created",
    "",
    (
        .[] | " * [\(.filename)](\(.url))"
    ),
    "", 
    "Verify with `gh attestation verify --repo \($repo) --predicate-type https://docs.pypi.org/attestations/publish/v1 [FILENAME]`"
]
| join("\n")

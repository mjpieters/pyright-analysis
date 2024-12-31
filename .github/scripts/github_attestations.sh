#!/bin/bash
per_attestation=()
for bundle in dist/*.sigstore; do
  filename="$(basename "${bundle%.sigstore}")"
  attestation_id=$(
    jq --compact-output '{"bundle":.}' "$bundle" \
      | gh api \
        --method POST \
        -H "Accept: application/vnd.github+json" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        '/repos/{owner}/{repo}/attestations' \
        --input - \
        --jq '.id'
  )
  # collate information into a JSON object per attestation
  per_attestation+=( "$(
    jq --null-input --compact-output \
      --arg attestation_id "$attestation_id" \
      --arg filename "$filename" \
      --arg server_url "$GITHUB_SERVER_URL" \
      --arg repository "$GITHUB_REPOSITORY" \
      '{filename: $filename, id: $attestation_id, url: "\($server_url)/\($repository)/attestations/\($attestation_id)"}'
  )" )
done
# collate the per-attestation JSON object into an array, and share it as step output
attestations="$(jq '[$ARGS.positional[]]' --compact-output --null-input --jsonargs "${per_attestation[@]}")"
echo "attestations=${attestations}" >> "$GITHUB_OUTPUT"

# extend the release notes with a thematic break to separate the attestations report
{
  echo
  echo '---'
  echo
} >> release_notes.md

# generate a summary for both the release notes and the step output
echo "$attestations" \
  | jq --raw-output --arg repo "$GITHUB_REPOSITORY" --from-file .github/scripts/attestations_report.jq \
  | tee -a release_notes.md "$GITHUB_STEP_SUMMARY"

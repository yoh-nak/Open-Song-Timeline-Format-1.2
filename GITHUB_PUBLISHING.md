# GitHub publishing guide / GitHub公開手順

1. Create a repository such as `OSTF` and select **Public**. The repository name is only a suggestion.
2. Extract `OSTF_v1.2_GitHub_Release.zip` locally. Do not upload the ZIP instead of extracting it.
3. From **Add file → Upload files**, drag the contained repository files/folders into GitHub's upload area. Files are kept below the requested 100-file unit; check the browser shows nested folders correctly.
4. Commit with `Release OSTF v1.2 Stable Core specification and examples`.
5. Optionally open **Releases → Draft a new release**, tag `v1.2.0`, title `OSTF v1.2 Stable Core`, attach the distribution ZIP and publish.
6. Verify the README, sample `.ostf` files and docs display correctly online. Do not promise support by particular DAWs.

If GitHub's website does not preserve folder uploads in your browser, use GitHub Desktop or Git (`git add .; git commit; git push`). A ZIP uploaded as a file is **not** automatically expanded into a GitHub repository.

The format has no software license grant inferred from its name. A `LICENSE` file has intentionally not been invented. Choose and add an appropriate license **before** inviting reuse, if you wish to grant permissions explicitly.

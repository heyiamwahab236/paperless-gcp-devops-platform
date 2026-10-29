# Publish a reviewable GitHub portfolio

The project repository is [heyiamwahab236/paperless-gcp-devops-platform](https://github.com/heyiamwahab236/paperless-gcp-devops-platform). This guide describes publishing another copy and maintaining the portfolio. The dated validation record describes the original local build; current workflow results are available in GitHub Actions. Do not commit generated credentials, raw logs or runtime data.

## Local review

Run the static validation path in the README. Inspect the current source and evidence. If using an extracted ZIP, initialize Git from the project root:

```bash
git init -b main
git status --short --ignored
git add .
git diff --cached --stat
git diff --cached --check
git diff --cached
```

Set your actual Git author name/email if Git asks; do not use a fabricated identity. Review staged files before committing. In particular, the staged paths must exclude `.secrets`, `.env`, `runtime`, `backups`, `.terraform`, `build`, state and saved plans. License texts and `terraform/.terraform.lock.hcl` **should** be present.

```bash
git commit -m "Add Paperless deployment and operations portfolio"
```

Create a new empty repository called `paperless-gcp-devops-platform` in your own GitHub account. Public makes it easy for employers to inspect, so first confirm that every staged file is suitable for public access. Do not initialize a conflicting README or license on GitHub. Replace `YOUR-USERNAME` below with your real account:

```bash
git remote add origin https://github.com/YOUR-USERNAME/paperless-gcp-devops-platform.git
git push -u origin main
```

These commands are instructions for your publication step; the placeholders are not working URLs.

## Repository presentation

Suggested description: “Local-first DevOps operations lab for upstream Paperless-ngx: Compose, Minikube/Helm, tested GCP Terraform blueprint, CI and evidence. No permanent cloud deployment.”

Suggested topics: `devops`, `portfolio`, `paperless-ngx`, `docker-compose`, `kubernetes`, `helm`, `terraform`, `google-cloud`, `github-actions`.

Enable Actions if prompted. `Validate` runs on main pushes and pull requests. From Actions, run `Runtime demo` for each target separately, and run `Image security`. The scheduled image scan runs on the default branch; GitHub may disable schedules on inactive public repositories. Hosted runner usage has its own account limits and billing settings even though these workflows do not use GCP. Use GitHub's usage controls and avoid enabling paid overages solely for the portfolio.

Only add a status badge after the repository exists. Use the workflow's actual badge URL from GitHub and link to its run history. Add completed evidence and real links to `docs/evidence/`; do not label local command output as a GitHub Actions run. Consider requiring the `validate` and `security` jobs in branch rules once they have run.

## Keep it credible

For a change, open a branch and a small PR with a concrete reason and relevant test results. Dependabot covers Actions, Python development dependencies and Terraform providers. Image digests, Minikube/Kubernetes pins and downloaded validation-tool versions need a deliberate review/update. Resolve an image tag to its real manifest digest, update all references, and run the runtime/security checks.

You can keep the GCP blueprint undeployed indefinitely. No public cloud URL or billing screenshot is needed to describe it accurately as infrastructure design and validation work.

# Tech Stack

This is a documentation-only review workspace. The "stack" is minimal.

## Toolchain

- **Shell**: POSIX-ish shell scripts (`sh`/`bash`) for fetching candidate git repos.
- **Docs**: Markdown. No static site generator, no build step.
- **Git**: Used to fetch candidates and to version this review repo itself.

## Infrastructure

None. No hosting, no CI/CD pipeline, no container runtime, no database, no message queue. The repo is consumed directly on disk.

## Notable absences

- No language runtime (Python, Node, Go, Rust) — the repo has no executable code.
- No package manager — no dependencies to install.
- No LSP config — no source files to type-check.

See `docs/ARCHITECTURE.md` for how this fits the C4 model.
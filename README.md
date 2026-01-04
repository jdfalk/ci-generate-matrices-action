# Generate CI Test Matrices Action

Generate language-specific CI test matrices based on repository configuration
with intelligent fallback handling and optional dockerized execution.

## Usage

```yaml
- name: Load config
  id: config
  uses: jdfalk/load-config-action@v1

- name: Generate CI matrices
  id: matrices
  uses: jdfalk/ci-generate-matrices-action@v1
  with:
    repository-config: ${{ steps.config.outputs.config }}
    include-linux: true
    include-macos: false

- name: Run Go tests
  if: fromJson(steps.matrices.outputs.go-matrix).go-version
  uses: actions/setup-go@v5
  with:
    go-version: ${{ matrix.go-version }}
```

### Force Docker Execution

```yaml
- uses: jdfalk/ci-generate-matrices-action@v1
  id: matrices
  with:
    use-docker: true
    docker-image: ghcr.io/jdfalk/ci-generate-matrices-action:main
```

## Inputs

| Input                         | Description                                                      | Default                                           |
| ----------------------------- | ---------------------------------------------------------------- | ------------------------------------------------- |
| `repository-config`           | Repository configuration as JSON                                 | `{}`                                              |
| `fallback-go-version`         | Fallback Go version                                              | `1.23`                                            |
| `fallback-python-version`     | Fallback Python version                                          | `3.12`                                            |
| `fallback-rust-version`       | Fallback Rust version                                            | `1.75`                                            |
| `fallback-node-version`       | Fallback Node.js version                                         | `22`                                              |
| `fallback-coverage-threshold` | Fallback coverage threshold                                      | `80`                                              |
| `include-linux`               | Include ubuntu-latest                                            | `true`                                            |
| `include-macos`               | Include macos-latest                                             | `false`                                           |
| `include-windows`             | Include windows-latest                                           | `false`                                           |
| `use-docker`                  | Run the action inside the published container image              | `false`                                           |
| `docker-image`                | Docker image reference (tag or digest) when `use-docker` is true | `ghcr.io/jdfalk/ci-generate-matrices-action:main` |

## Outputs

| Output               | Description                        |
| -------------------- | ---------------------------------- |
| `go-matrix`          | Go CI matrix as JSON               |
| `python-matrix`      | Python CI matrix as JSON           |
| `rust-matrix`        | Rust CI matrix as JSON             |
| `frontend-matrix`    | Frontend/Node.js CI matrix as JSON |
| `coverage-threshold` | Coverage threshold percentage      |

## Matrix Format

Each matrix includes `os` and language version arrays:

```json
{
  "go-version": ["1.23", "1.22"],
  "os": ["ubuntu-latest"]
}
```

Use with GitHub Actions matrix:

```yaml
strategy:
  matrix: ${{ fromJson(steps.matrices.outputs.go-matrix) }}
```

## Features

✅ **Config-Driven** - Reads versions from repository config ✅ **Fallback
Handling** - Intelligent defaults when config missing ✅ **Multi-Platform** -
Select which OSes to include ✅ **Coverage Thresholds** - Propagate coverage
requirements ✅ **JSON Output** - Direct integration with matrix jobs

## Related Actions

- [load-config-action](https://github.com/jdfalk/load-config-action) - Load
  repository config
- [detect-languages-action](https://github.com/jdfalk/detect-languages-action) -
  Detect project languages

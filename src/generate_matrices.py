#!/usr/bin/env python3
# file: src/generate_matrices.py
# version: 1.0.0
# guid: 5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9a0b

"""Generate CI test matrices for Go, Python, Rust, and Node.js"""

import json
import os


def write_output(name, value):
    """Write to GITHUB_OUTPUT."""
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"{name}={value}\n")


def write_summary(text):
    """Write to GITHUB_STEP_SUMMARY."""
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write(text + "\n")


def main():
    # Parse config
    config_json = os.environ.get("REPOSITORY_CONFIG", "{}")
    config = json.loads(config_json)
    ci_config = config.get("ci", {})

    # Build OS list
    oses = []
    if os.environ.get("INCLUDE_LINUX", "true").lower() == "true":
        oses.append("ubuntu-latest")
    if os.environ.get("INCLUDE_MACOS", "false").lower() == "true":
        oses.append("macos-latest")
    if os.environ.get("INCLUDE_WINDOWS", "false").lower() == "true":
        oses.append("windows-latest")

    # Generate Go matrix
    go_versions = ci_config.get("go", {}).get("versions", [os.environ.get("FALLBACK_GO_VERSION", "1.23")])
    go_matrix = {
        "go-version": go_versions,
        "os": oses
    }
    write_output("go-matrix", json.dumps(go_matrix, separators=(",", ":")))

    # Generate Python matrix
    python_versions = ci_config.get("python", {}).get("versions", [os.environ.get("FALLBACK_PYTHON_VERSION", "3.12")])
    python_matrix = {
        "python-version": python_versions,
        "os": oses
    }
    write_output("python-matrix", json.dumps(python_matrix, separators=(",", ":")))

    # Generate Rust matrix
    rust_versions = ci_config.get("rust", {}).get("versions", [os.environ.get("FALLBACK_RUST_VERSION", "1.75")])
    rust_matrix = {
        "rust-version": rust_versions,
        "os": oses
    }
    write_output("rust-matrix", json.dumps(rust_matrix, separators=(",", ":")))

    # Generate Node.js matrix
    node_versions = ci_config.get("frontend", {}).get("node-versions", [os.environ.get("FALLBACK_NODE_VERSION", "22")])
    frontend_matrix = {
        "node-version": node_versions,
        "os": oses
    }
    write_output("frontend-matrix", json.dumps(frontend_matrix, separators=(",", ":")))

    # Coverage threshold
    coverage_threshold = ci_config.get("coverage", {}).get("threshold", os.environ.get("FALLBACK_COVERAGE_THRESHOLD", "80"))
    write_output("coverage-threshold", str(coverage_threshold))

    # Summary
    write_summary("## 🔧 Generated CI Matrices")
    write_summary(f"- **Go versions:** {', '.join(go_versions)}")
    write_summary(f"- **Python versions:** {', '.join(python_versions)}")
    write_summary(f"- **Rust versions:** {', '.join(rust_versions)}")
    write_summary(f"- **Node.js versions:** {', '.join(node_versions)}")
    write_summary(f"- **Operating systems:** {', '.join(oses)}")
    write_summary(f"- **Coverage threshold:** {coverage_threshold}%")

    print("✅ Matrices generated successfully")


if __name__ == "__main__":
    main()

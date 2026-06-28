# Health Monitor

An extensible system health-checking framework with a pluggable check architecture, YAML configuration, and automatic email alerting.

## What it does

- Runs a configurable set of health checks (system resources, processes, network ports)
- Each check is enabled/disabled independently via configuration, without removing it
- Supports multiple instances of the same check type (e.g. multiple disk paths, processes, or ports)
- Sends an email alert listing all failed checks when a run completes
- Includes a custom Prometheus-compatible metrics exporter for integration with Grafana

## Architecture

The system is built around a plugin-style check architecture:

\`\`\`
monitor.py              → orchestration: loads config, runs all checks, sends alerts
checks/
├── base.py              → abstract Check class and CheckResult data structure
├── system_checks.py      → CPU / RAM / Disk threshold checks
├── process_check.py      → verifies a process is running (by name or command line)
├── port_check.py         → verifies a TCP port is open and accepting connections
└── registry.py           → maps config "type" strings to check classes
exporter.py              → exposes metrics in native Prometheus text format
\`\`\`

Each check is a class implementing a common `run()` interface, returning a standardized `CheckResult` (ok/fail, value, message). New check types can be added by creating a new class and registering it in `registry.py` — no changes needed to the orchestration logic in `monitor.py`.

## Adding a new check type

1. Create a new class in `checks/` extending `Check`, implementing `run()`
2. Register it in `checks/registry.py`'s `CHECK_REGISTRY` dictionary
3. Add a new entry under `checks:` in `config.yml` with the matching `type`

## Installation

\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
\`\`\`

## Configuration

\`\`\`bash
cp config.example.yml config.yml
\`\`\`

Edit `config.yml` with your real email credentials and desired checks. Each check entry supports `enabled: true/false` to toggle it without deleting it from the file:

\`\`\`yaml
checks:
  - type: cpu_threshold
    threshold: 85
    enabled: true

  - type: disk_threshold
    threshold: 90
    path: "/"
    enabled: true

  - type: process_running
    pattern: "WebSphere"
    enabled: false
\`\`\`

**Note:** `config.yml` is excluded via `.gitignore` — no real credentials are present in this repo.

## Available check types

| Type | Config fields | Description |
|---|---|---|
| `cpu_threshold` | `threshold` | Fails if CPU usage exceeds threshold (%) |
| `ram_threshold` | `threshold` | Fails if RAM usage exceeds threshold (%) |
| `disk_threshold` | `threshold`, `path` | Fails if disk usage on `path` exceeds threshold (%) |
| `process_running` | `pattern` | Fails if no process matches the given name/cmdline pattern |
| `port_open` | `host`, `port`, `timeout` (optional) | Fails if the TCP port is not accepting connections. Distinguishes `refused` (service likely down) from `timeout` (possible network/firewall issue) |

## Running

\`\`\`bash
python3 monitor.py
\`\`\`

Logs are written to `monitor.log`. Recommended to run on a schedule via cron:

\`\`\`
*/5 * * * * cd /path/to/health-monitor && /path/to/health-monitor/venv/bin/python3 monitor.py
\`\`\`

## Prometheus exporter (bonus)

A custom-built metrics exporter (`exporter.py`) exposes system metrics in native Prometheus text format, independent of the main check framework:

\`\`\`bash
uvicorn exporter:app --host 0.0.0.0 --port 9100
curl http://localhost:9100/metrics
\`\`\`

Tested end-to-end with a live Prometheus + Grafana stack.

## Sample log output

\`\`\`
2026-06-28 18:39:59,828 - INFO - [OK] cpu_threshold: CPU at 14.3% (threshold 85%)
2026-06-28 18:39:59,828 - INFO - [OK] ram_threshold: RAM at 28.1% (threshold 85%)
2026-06-28 18:39:59,828 - INFO - [OK] disk_threshold: Disk at 7.9% on / (threshold 90%)
\`\`\`

## Production Considerations

This project currently runs as the executing user with credentials in a local config file. For a production deployment, the following would be required:

### Dedicated service account

Running as a dedicated low-privilege system user rather than a regular login account:

\`\`\`bash
sudo useradd -r -s /usr/sbin/nologin monitorsvc
\`\`\`

### Config file permissions

`config.yml` contains email credentials and should be restricted to owner-only access:

\`\`\`bash
chmod 600 config.yml
\`\`\`

### Scaling to many hosts

The current implementation is single-host. The Prometheus exporter pattern (`exporter.py`) is the intended path toward multi-host monitoring: each host runs its own exporter, and a central Prometheus instance scrapes all of them, aggregating results in Grafana rather than relying on per-host email alerts.
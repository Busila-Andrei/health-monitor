# System Health Monitor

A Python script for monitoring system resources (CPU, RAM, disk), with automatic email alerts when values exceed a configured threshold.

## What it does

- Reads CPU, RAM, and disk usage every 5 minutes (via cron)
- Writes results to a structured log file, with timestamps
- Sends an email alert if any value exceeds the configured threshold

## Tech stack

- Python 3
- psutil (system metrics)
- smtplib (email alerts)
- cron (scheduled execution)

## Installation

\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip install psutil
\`\`\`

## Configuration

1. Copy `config.example.json` to `config.json`
2. Fill in your real values (email, app password, thresholds)

\`\`\`bash
cp config.example.json config.json
\`\`\`

**Note:** `config.json` is excluded via `.gitignore` — no real credentials are present in this repo.

## Manual run

\`\`\`bash
python3 monitor.py
\`\`\`

## Scheduled run (cron)

\`\`\`
*/5 * * * * cd /path/to/health-monitor && /path/to/health-monitor/venv/bin/python3 monitor.py
\`\`\`

## Sample log output

\`\`\`
2026-06-27 20:44:23,272 - INFO - CPU=7.3% RAM=21.6% Disk=6.9%
\`\`\`

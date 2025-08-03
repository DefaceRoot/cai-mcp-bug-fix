# CAI MCP Bug Fix

Fixes the `'StdioServerParameters' object has no attribute 'get'` error in [Cybersecurity AI (CAI)](https://github.com/aliasrobotics/cai) that prevents the `/mcp add` command from working with STDIO MCP servers.

## The Problem

When using CAI with MCP (Model Context Protocol) servers via STDIO transport, the `/mcp add` command fails with:

## The Solution

This script automatically fixes the bug by replacing `server.params.get()` calls with `getattr(server.params, ...)` throughout the CAI codebase.

## Usage

1. Make sure CAI is installed: `pip install cai-framework`
2. Download and run the fix:
```bash
wget https://raw.githubusercontent.com/DefaceRoot/cai-mcp-bug-fix/main/fix_cai_mcp_bug.py
python fix_cai_mcp_bug.py

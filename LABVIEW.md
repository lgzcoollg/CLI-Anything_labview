# LabVIEW CLI - Standard Operating Procedure

## Purpose

This document defines the architecture and operating procedures for the LabVIEW CLI harness. It allows AI agents to control LabVIEW (VIs, projects, builds) via a standardized command-line interface.

## Installation

### Prerequisites
- **LabVIEW 2014 or later**: Must be installed on the system. The `LabVIEWCLI` tool is included with LabVIEW Full and Professional Development Systems.
- **Python 3.10+**: Required to run the harness.

### Setup
1. Navigate to the harness directory:
   ```bash
   cd ./
   ```

2. Install the package in editable mode:
   ```bash
   pip install -e .
   ```

3. Verify installation:
   ```bash
   cli-anything-labview locate
   ```
   If the CLI is not found automatically, refer to the [Configuration](#configuration) section.

## Architecture

### Backend Engine

- **Executable**: `LabVIEWCLI` (NI LabVIEW Command Line Interface)
- **Primary Interface**: Invokes operations (ExecuteBuildSpec, RunVI, etc.)
- **Data Model**: `.vi` (Virtual Instruments), `.lvproj` (Project files), `.ctl` (Controls)
- **Platform**: macOS (requires explicit path to LabVIEW.app), Windows, Linux

### Command Groups

1. **Project Management** (`project`)
   - Build specifications (`project build`)

2. **VI Execution** (`vi`)
   - Run specific VIs (`vi run`)
   - Pass input parameters

3. **Configuration & Diagnostics**
   - Locate CLI executable (`locate`)
   - Set LabVIEW version via `--year`

## Implementation Details

### Path Resolution
The harness employs a robust strategy to find the `LabVIEWCLI` executable on macOS:
1.  **Environment Variable**: Checks `LABVIEW_CLI_PATH`.
2.  **Standard Paths**: Checks common installation directories:
    - `/Applications/National Instruments/LabVIEW <year>/LabVIEW CLI/LabVIEWCLI`
    - `/Library/Application Support/National Instruments/LabVIEW CLI/LabVIEWCLI` (Common location)
3.  **System Search**: Uses `mdfind` (Spotlight) as a fallback to locate the executable anywhere on the system.

### Command Structure

```bash
cli-anything-labview [OPTIONS] COMMAND [ARGS]...
```

**Global Options:**
- `--year <year>`: Specify LabVIEW version (e.g., 2024, 2023). Optional.
- `--json`: Output results in JSON format for Agent consumption.

<a id="configuration"></a>
**Configuration:**

You can configure the LabVIEW CLI path using the `LABVIEW_CLI_PATH` environment variable if the automatic detection fails.

```bash
# Example
export LABVIEW_CLI_PATH="/Applications/National Instruments/LabVIEW 2024 64-bit/LabVIEW CLI/LabVIEWCLI"
```

**Commands:**

*   **Locate CLI**:
    ```bash
    cli-anything-labview locate
    ```

*   **Run VI**:
    ```bash
    cli-anything-labview vi run /path/to/test.vi "arg1" "arg2"
    ```

*   **Build Project**:
    ```bash
    cli-anything-labview project build /path/to/project.lvproj "Build Specification Name" --target "My Computer"
    ```

## Testing Strategy

- **Unit Tests**: Mock `subprocess.run` to simulate `LabVIEWCLI` responses.
- **E2E Tests**: Requires local LabVIEW installation. Verify real execution of simple VIs.

# OpenWebUI Project

This project sets up OpenWebUI using `uv` for fast and reliable Python package management.

## Prerequisites

- Python 3.11 or 3.12 (Python 3.13 is not supported by OpenWebUI)
- `uv` package manager installed

### Installing uv

If you don't have `uv` installed, run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or on Windows, you can also use:

```powershell
pip install uv
```

## Quick Start

### 1. Initial Setup

Run the setup script to create the virtual environment and install dependencies:

```powershell
.\setup.ps1
```

This will:
- Create a virtual environment using `uv`
- Install OpenWebUI and its dependencies
- Set up the project structure

### 2. Run OpenWebUI

You can run OpenWebUI in two ways:

**Option A: Using the run script (recommended)**
```powershell
.\run.ps1
```

**Option B: Manual activation**
```powershell
.\.venv\Scripts\Activate.ps1
open-webui serve
```

### 3. Access OpenWebUI

Once running, OpenWebUI will be available at:
- **URL**: http://localhost:8080
- Open it in your web browser

Press `Ctrl+C` to stop the server.

## Configuration

### Data Directory

By default, OpenWebUI stores data in its default location. To customize the data directory, edit `run.ps1` and uncomment/modify the `DATA_DIR` environment variable:

```powershell
$env:DATA_DIR = "$PWD\data"
```

### Python Version

The project is configured to use Python 3.11 (specified in `.python-version`). To use Python 3.12, change the version in `.python-version` and recreate the virtual environment:

```powershell
uv venv --python 3.12
uv pip install -e .
```

## Project Structure

```
.
├── .venv/              # Virtual environment (created by uv)
├── .python-version     # Python version specification
├── pyproject.toml      # Project dependencies and metadata
├── setup.ps1           # Setup script
├── run.ps1             # Run script
└── README.md           # This file
```

## Managing Dependencies

### Adding Dependencies

To add new dependencies, edit `pyproject.toml` and run:

```powershell
uv pip install -e .
```

### Updating Dependencies

To update OpenWebUI to the latest version:

```powershell
uv pip install --upgrade open-webui
```

## Troubleshooting

### Virtual Environment Issues

If you encounter issues with the virtual environment, you can recreate it:

```powershell
Remove-Item -Recurse -Force .venv
.\setup.ps1
```

### Port Already in Use

If port 8080 is already in use, you can specify a different port:

```powershell
open-webui serve --port 8081
```

### Python Version Issues

Make sure you have Python 3.11 or 3.12 installed. Check your Python version:

```powershell
python --version
```

## Additional Resources

- [OpenWebUI Documentation](https://docs.openwebui.com/)
- [OpenWebUI GitHub](https://github.com/open-webui/open-webui)
- [uv Documentation](https://docs.astral.sh/uv/)

## License

This project uses OpenWebUI, which is licensed under the Apache License 2.0.

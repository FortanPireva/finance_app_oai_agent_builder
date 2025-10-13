# uv Development Guide

Complete guide to using `uv` with the FinTech Support Chatbot project.

## What is uv?

`uv` is an extremely fast Python package installer and resolver, written in Rust by Astral (the creators of Ruff). It's designed to be a drop-in replacement for pip, but 10-100x faster.

### Key Benefits
- ⚡ 10-100x faster than pip
- 🔒 Better dependency resolution
- 💾 Efficient caching
- 🎯 Compatible with pip requirements
- 🚀 Built in Rust for maximum performance

## Installation

### Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv

# Or with pip (ironically)
pip install uv

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Verify Installation

```bash
uv --version
# Should output: uv 0.x.x
```

## Project Setup with uv

### Initial Setup

```bash
# Clone the project
git clone <repo-url>
cd finance_app

# Run the setup script (uses uv automatically)
chmod +x setup.sh
./setup.sh
```

### Manual Setup

```bash
# Create virtual environment
uv venv

# Activate it
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -r requirements.txt
```

## Common Commands

### Package Management

```bash
# Install a package
uv pip install fastapi

# Install specific version
uv pip install fastapi==0.104.1

# Install multiple packages
uv pip install fastapi uvicorn openai

# Install from requirements.txt
uv pip install -r requirements.txt

# Install with extras
uv pip install "fastapi[all]"
```

### Package Information

```bash
# List installed packages
uv pip list

# Show package details
uv pip show fastapi

# Check outdated packages
uv pip list --outdated

# Generate requirements.txt
uv pip freeze > requirements.txt
```

### Package Updates

```bash
# Update a specific package
uv pip install --upgrade fastapi

# Update all packages
uv pip install --upgrade -r requirements.txt

# Reinstall a package
uv pip install --force-reinstall fastapi
```

### Package Removal

```bash
# Uninstall a package
uv pip uninstall fastapi

# Uninstall all packages
uv pip freeze | xargs uv pip uninstall -y
```

## Running the Application with uv

### Method 1: Direct Execution

```bash
# Run uvicorn directly
uv run uvicorn main:app --reload

# Run with custom port
uv run uvicorn main:app --reload --port 8080

# Run a Python script
uv run python run.py
```

### Method 2: Using Scripts

```bash
# Development server (recommended)
./dev.sh

# Or manually
uv run uvicorn main:app --reload --port 8000
```

### Method 3: After Activation

```bash
# Activate virtual environment first
source .venv/bin/activate

# Then run normally
uvicorn main:app --reload
python run.py
```

## Working with pyproject.toml

Our project uses `pyproject.toml` for cleaner dependency management:

```toml
[project]
name = "finance-support-chatbot"
version = "1.0.0"
requires-python = ">=3.9"
dependencies = [
    "fastapi==0.104.1",
    "uvicorn[standard]==0.24.0",
    # ... more dependencies
]
```

### Install from pyproject.toml

```bash
# Install project dependencies
uv pip install -e .

# Or just the dependencies
uv pip install -r requirements.txt
```

## Speed Comparisons

### Real-World Benchmarks

```bash
# Traditional pip
time pip install -r requirements.txt
# ~ 45-120 seconds

# With uv
time uv pip install -r requirements.txt
# ~ 3-8 seconds

# That's 10-40x faster! ⚡
```

### Why So Fast?

1. **Parallel Downloads**: Downloads multiple packages simultaneously
2. **Rust Implementation**: Native code vs Python
3. **Better Caching**: Smarter cache management
4. **Optimized Resolution**: Faster dependency resolution algorithm

## Development Workflow

### Starting a New Work Session

```bash
# 1. Pull latest changes
git pull

# 2. Update dependencies (super fast with uv!)
uv pip install -r requirements.txt

# 3. Run the app
./dev.sh
```

### Adding a New Dependency

```bash
# 1. Install the package
uv pip install new-package

# 2. Update requirements
uv pip freeze > requirements.txt

# 3. Test your changes
uv run python -m pytest

# 4. Commit
git add requirements.txt
git commit -m "Add new-package"
```

### Updating Dependencies

```bash
# Check what's outdated
uv pip list --outdated

# Update specific package
uv pip install --upgrade package-name

# Update all
uv pip install --upgrade -r requirements.txt

# Save updates
uv pip freeze > requirements.txt
```

## Virtual Environment Management

### Creating Environments

```bash
# Create a new venv
uv venv

# Create with specific Python version
uv venv --python 3.11

# Create in custom location
uv venv custom_env
```

### Activating Environments

```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# Fish shell
source .venv/bin/activate.fish
```

### Deactivating

```bash
deactivate
```

### Cleaning Up

```bash
# Remove virtual environment
rm -rf .venv

# Recreate fresh
uv venv
uv pip install -r requirements.txt
```

## Troubleshooting with uv

### "uv: command not found"

```bash
# Re-install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (if needed)
export PATH="$HOME/.cargo/bin:$PATH"
```

### Cache Issues

```bash
# Clear uv cache
uv cache clean

# Reinstall package
uv pip install --force-reinstall package-name
```

### Version Conflicts

```bash
# Show dependency tree
uv pip list

# Install with verbose output
uv pip install -v package-name

# Force specific version
uv pip install "package-name==X.Y.Z"
```

### Virtual Environment Issues

```bash
# Delete and recreate
rm -rf .venv
uv venv
uv pip install -r requirements.txt
```

## Advanced Usage

### Compile Requirements

```bash
# Create a lock file (coming soon to uv)
uv pip compile requirements.in > requirements.txt
```

### Sync Environment

```bash
# Install exact versions from requirements.txt
uv pip sync requirements.txt
```

### Isolated Runs

```bash
# Run without activating venv
uv run --isolated python script.py
```

## Best Practices

### 1. Always Use uv for Package Operations

```bash
# ✅ Good
uv pip install package-name

# ❌ Avoid
pip install package-name
```

### 2. Keep Requirements Updated

```bash
# After any pip install
uv pip freeze > requirements.txt
```

### 3. Use pyproject.toml for Dependencies

Keep `pyproject.toml` as source of truth, generate `requirements.txt` from it.

### 4. Leverage Speed for CI/CD

```yaml
# .github/workflows/test.yml
- name: Install dependencies
  run: |
    pip install uv
    uv pip install -r requirements.txt
```

### 5. Cache uv Downloads

uv automatically caches downloads, making repeated installs even faster!

## Comparison: pip vs uv

| Feature               | pip         | uv               | Winner |
| --------------------- | ----------- | ---------------- | ------ |
| Speed                 | Baseline    | 10-100x faster   | 🏆 uv   |
| Dependency Resolution | Good        | Better           | 🏆 uv   |
| Cache Management      | Basic       | Advanced         | 🏆 uv   |
| Compatibility         | Native      | 100% compatible  | 🤝 Tie  |
| Maturity              | Very mature | Growing          | pip    |
| Installation          | Built-in    | Separate install | pip    |

## Integration with Other Tools

### With Docker

```dockerfile
FROM python:3.11-slim

# Install uv
RUN pip install uv

# Copy requirements
COPY requirements.txt .

# Install dependencies with uv
RUN uv pip install --system -r requirements.txt

# ... rest of Dockerfile
```

### With Vercel

Vercel's Python runtime can use uv:

```json
{
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    }
  ]
}
```

### With GitHub Actions

```yaml
- name: Install uv
  run: pip install uv

- name: Install dependencies
  run: uv pip install -r requirements.txt
```

## Performance Tips

### 1. Use uv for Everything

Even one-off installs benefit from uv's speed:

```bash
uv pip install ipython  # Much faster!
```

### 2. Leverage Parallel Downloads

uv automatically downloads packages in parallel. No configuration needed!

### 3. Keep Cache Warm

uv's cache persists across projects, making subsequent installs instant.

### 4. Use Virtual Environments

Always use venvs to avoid system package conflicts:

```bash
uv venv && source .venv/bin/activate
```

## Migrating from pip to uv

### Step 1: Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Replace Commands

| pip command     | uv equivalent      |
| --------------- | ------------------ |
| `pip install`   | `uv pip install`   |
| `pip uninstall` | `uv pip uninstall` |
| `pip freeze`    | `uv pip freeze`    |
| `pip list`      | `uv pip list`      |
| `pip show`      | `uv pip show`      |

### Step 3: Update Scripts

```bash
# Before
pip install -r requirements.txt

# After
uv pip install -r requirements.txt
```

### Step 4: Enjoy Speed! ⚡

Your installations are now 10-100x faster!

## Resources

- **uv GitHub**: https://github.com/astral-sh/uv
- **Documentation**: https://github.com/astral-sh/uv#readme
- **Astral Blog**: https://astral.sh/blog
- **Releases**: https://github.com/astral-sh/uv/releases

## Quick Reference Card

```bash
# Setup
uv venv                              # Create virtual environment
source .venv/bin/activate            # Activate environment

# Install
uv pip install package               # Install package
uv pip install -r requirements.txt   # Install from requirements
uv pip install --upgrade package     # Update package

# Information
uv pip list                          # List packages
uv pip show package                  # Show package info
uv pip freeze > requirements.txt     # Save dependencies

# Run
uv run python script.py              # Run Python script
uv run uvicorn main:app --reload     # Run web server

# Maintenance
uv pip install --upgrade -r requirements.txt  # Update all
uv cache clean                       # Clear cache
```

## Summary

Using `uv` with this project gives you:

- ⚡ **10-100x faster** package installations
- 🔒 **Better dependency** resolution
- 💾 **Efficient caching** across projects
- 🎯 **100% compatibility** with pip
- 🚀 **Modern tooling** for Python development

**Bottom Line**: Replace `pip` with `uv pip` in all your commands and enjoy the speed boost!

---

**Happy Fast Coding with uv! ⚡**


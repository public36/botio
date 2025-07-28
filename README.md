# Botio Auto Updater

This project contains scripts to automatically update your bot repository from GitHub, run code linting, push fixes, update product list, and trigger Netlify build hook to refresh your site.

## Files

- `bot_updater.py`: Main bot script that clones/pulls your GitHub repo, runs flake8 for linting, commits & pushes fixes, and triggers Netlify rebuild every 10 minutes.
- `update_products.py`: Script to add a new product daily to `products.json` and trigger Netlify build.
- `products.json`: JSON file to store your products data (create empty or with sample data).
- `requirements.txt`: Python dependencies.
- `README.md`: This file.

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
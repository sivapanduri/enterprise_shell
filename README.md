# Enterprise Shell

Reusable Flask + Jinja enterprise shell for future business platforms.

## Stage 1 included

- Flask app factory
- Config classes
- Extension registry
- Public blueprint
- Base/public layouts
- Landing page
- About page
- Status page

## Quick start

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
export FLASK_ENV=development
python manage.py
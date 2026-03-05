# ClarityScan Django App

Django web app with:
- User signup/login/logout
- Keras LSTM-backed text classification endpoint
- Per-user prediction history

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Model assets

Place your existing model artifacts in `ml_assets/`:
- `model.keras` (required)
- `tokenizer.pkl` (required)
- `labels.json` (optional, JSON list of class names)
- `max_len.txt` (optional, integer sequence length; defaults to 200)

## App routes

- `/signup/` create account
- `/login/` log in
- `/` classify text
- `/history/` view your own prediction history

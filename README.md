# K.O.C Collections

K.O.C Collections contains the public storefront and an optional Flask admin backend. The admin backend is not run by GitHub Pages; deploy it to a Python host with persistent disk storage for its SQLite database.

## Run locally

Open `index.html` in a browser, or serve this folder with any static web server.

To run the Flask admin backend, install `requirements.txt` and set these environment variables before starting `server.py`:

- `KOC_SECRET_KEY`: a long, random secret used to sign sessions.
- `KOC_ADMIN1_USERNAME` and `KOC_ADMIN1_PASSWORD`: credentials for the first admin.
- `KOC_ADMIN2_USERNAME` and `KOC_ADMIN2_PASSWORD`: credentials for the second admin.

For example, in PowerShell:

```powershell
$env:KOC_SECRET_KEY = "<random-secret>"
$env:KOC_ADMIN1_USERNAME = "<admin-one-username>"
$env:KOC_ADMIN1_PASSWORD = "<unique-password>"
$env:KOC_ADMIN2_USERNAME = "<admin-two-username>"
$env:KOC_ADMIN2_PASSWORD = "<unique-password>"
python server.py
```

The admin accounts are created the first time the database is initialized. Keep these values out of source control. The SQLite database remains ignored.

## Publish with GitHub Pages

In the repository settings, enable GitHub Pages for the `main` branch and the root folder to publish the static storefront. GitHub Pages does not run the Flask login or admin dashboard.

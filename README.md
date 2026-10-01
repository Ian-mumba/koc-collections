# K.O.C Collections

K.O.C Collections contains the public storefront and an optional Flask admin backend. The admin backend is not run by GitHub Pages; deploy it to a Python host with persistent disk storage for its SQLite database.

## Run locally

Serve this folder over HTTP so the browser can load `products.json`:

```powershell
python -m http.server 8000
```

Then open `http://localhost:8000/`.

## Update products

Open [Pages CMS](https://app.pagescms.org/) and sign in with the GitHub account that owns this repository. Install its GitHub App for this repository when prompted, then select `koc-collections` and open **Products**. Add or edit product names, prices, categories, and images; saving commits the catalog and uploaded images to GitHub. GitHub Pages redeploys the storefront from those files.

The **Manage products** link in the site footer opens Pages CMS. The first visit requires GitHub sign-in and repository access authorization.

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

GitHub Pages publishes the static storefront from the `main` branch and root folder. It does not run the optional Flask login or admin dashboard. The database and session secret remain private runtime configuration.

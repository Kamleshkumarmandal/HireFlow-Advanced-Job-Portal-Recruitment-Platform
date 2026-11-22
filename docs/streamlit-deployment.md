# Deploy the HireFlow Streamlit demo

The repository keeps the original Next.js application and adds a separate Streamlit portfolio demo at the repository root.

## Run locally

Use Python 3.12 or newer.

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
```

macOS / Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud

1. Sign in to [Streamlit Community Cloud](https://share.streamlit.io) using the GitHub account that can access this public repository.
2. Select **Create app** and choose an existing repository.
3. Repository: `Kamleshkumarmandal/HireFlow-Advanced-Job-Portal-Recruitment-Platform`.
4. Branch: `main`.
5. Main file path: `streamlit_app.py`.
6. Choose an app URL/subdomain if Streamlit offers the option.
7. Select **Deploy** and wait for the app to finish building.
8. Copy the public `https://....streamlit.app` URL shown by Streamlit.

The Streamlit app does not need secrets for this sample-data demo. Do not paste GitHub passwords, tokens, or private keys into the app.

## Add the generated public URL to this README

After deployment, replace the **Not deployed yet** status in the README with the exact URL shown by Streamlit Cloud. Do not guess the URL before Streamlit creates the app.

## Demo limitations

Jobs, saved roles, application records, application-status changes and recruiter-created listings use Streamlit session state. They are sample data and are not persistent across restarts. The Next.js app's existing Supabase schema is not connected to this Streamlit interface. Login, real candidate accounts, resume storage, email notifications and live vacancies are not implemented in this demo.

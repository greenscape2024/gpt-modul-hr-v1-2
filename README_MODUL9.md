# MODUL 9 – Traženje poslova (Integracija)

Ova skripta (`modul9_job_search.py`) omogućuje korisniku da:
- Odabere zemlje i jezike
- Unese ključne riječi
- Dobije klikabilne linkove za traženje poslova po državama
- Generira JSON kriterij pretrage
- Prikaže korisničku uputu

## 🔧 Kako integrirati u postojeći projekt

1. Smjesti `modul9_job_search.py` u root direktorij Streamlit projekta ili pod `/modules/`
2. U `app.py` dodaj:

```python
from modul9_job_search import *  # ili import modul9_job_search ako želiš eksplicitno pozivanje
```

3. Ako koristiš `render_module()`, dodaj:

```python
elif active_module == "modul_9":
    import modul9_job_search  # Automatski poziva Streamlit sučelje
```

## 🧠 Napomena
Ova verzija koristi statičke linkove. Planirano je povezivanje s API servisima i lokalnom JSON bazom `job_sources_database.json`.

© 2025 Hrvoje Šajković

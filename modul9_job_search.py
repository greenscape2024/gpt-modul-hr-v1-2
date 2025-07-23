import streamlit as st
import datetime
import json

st.title("🔍 MODUL 9 – Traženje poslova po državama")

# Unos jezika i lokacija
keywords = st.text_input("Koje poslove tražiš? (npr. financial analyst, EU consultant...)", "financial analyst, EU consultant, M&A advisory")
selected_locations = st.multiselect(
    "Odaberi zemlje ili gradove za pretragu",
    ["Zagreb", "Remote", "Beč", "Ljubljana", "Bruxelles", "Frankfurt", "Amsterdam", "Prag"]
)

languages = st.text_input("Koje jezike govoriš?", "Hrvatski, Engleski")

if st.button("🔗 Generiraj linkove i JSON"):
    portal_links = {
        "Zagreb": [
            ("MojPosao", "https://www.moj-posao.net/"),
            ("Posao.hr", "https://www.posao.hr/"),
            ("HZZ burza rada", "https://burzarada.hzz.hr/"),
            ("LinkedIn HR", "https://www.linkedin.com/jobs/search/?location=Zagreb%2C%20Hrvatska")
        ],
        "Remote": [
            ("Remote OK", "https://remoteok.com/"),
            ("We Work Remotely", "https://weworkremotely.com/"),
            ("FlexJobs", "https://www.flexjobs.com/"),
            ("Working Nomads", "https://www.workingnomads.co/jobs"),
            ("LinkedIn Remote", "https://www.linkedin.com/jobs/search/?f_WT=2")
        ],
        "Beč": [
            ("Karriere.at", "https://www.karriere.at/"),
            ("Stepstone.at", "https://www.stepstone.at/"),
            ("LinkedIn Austria", "https://www.linkedin.com/jobs/search/?location=Austria")
        ],
        "Ljubljana": [
            ("MojeDelo", "https://www.mojedelo.com/"),
            ("Zaposlitev.net", "https://www.zaposlitev.net/"),
            ("LinkedIn Slovenia", "https://www.linkedin.com/jobs/search/?location=Slovenia")
        ],
        "Bruxelles": [
            ("Jobs.Euractiv", "https://jobs.euractiv.com/"),
            ("Stepstone.be", "https://www.stepstone.be/"),
            ("LinkedIn Belgium", "https://www.linkedin.com/jobs/search/?location=Belgium")
        ],
        "Frankfurt": [
            ("Stepstone.de", "https://www.stepstone.de/"),
            ("Indeed.de", "https://de.indeed.com/"),
            ("Arbeitsagentur", "https://www.arbeitsagentur.de/jobsuche/"),
            ("LinkedIn Germany", "https://www.linkedin.com/jobs/search/?location=Germany")
        ],
        "Amsterdam": [
            ("Indeed.nl", "https://www.indeed.nl/"),
            ("Intermediair", "https://www.intermediair.nl/"),
            ("LinkedIn Netherlands", "https://www.linkedin.com/jobs/search/?location=Netherlands")
        ],
        "Prag": [
            ("Jobs.cz", "https://www.jobs.cz/"),
            ("Prace.cz", "https://www.prace.cz/"),
            ("Expats.cz", "https://www.expats.cz/jobs/"),
            ("LinkedIn Czechia", "https://www.linkedin.com/jobs/search/?location=Czechia")
        ]
    }

    st.subheader("📌 Linkovi za portale za pretragu:")
    for loc in selected_locations:
        if loc in portal_links:
            st.markdown(f"**{loc}:**")
            for name, url in portal_links[loc]:
                st.markdown(f"- [{name}]({url})")

    search_criteria = {
        "keywords": keywords,
        "preferred_locations": selected_locations,
        "languages": languages.split(","),
        "timestamp": datetime.datetime.now().isoformat()
    }

    st.subheader("🧾 JSON kriteriji pretrage:")
    st.json(search_criteria)

    st.info("➡️ Upute: Otvori link, unesi jednu od ključnih riječi u tražilicu i filtriraj po lokaciji ako je moguće.")

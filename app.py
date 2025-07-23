# app.py – kompletna verzija s modulima 0 do 8 + navigacija i hero gumbi

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import os
from difflib import SequenceMatcher
import modul9_job_search

st.set_page_config(page_title="GPT MODUL – Navigacija", layout="centered")

st.title("📊 GPT MODUL – HR AI Career Assistant v1.2")
st.caption("© 2025 Hrvoje Šajković | powered by GPT AI")

# 🎛️ HERO GUMBI
st.markdown("## 🚀 Brzi pristup")
cols = st.columns(3)

with cols[0]:
    if st.button("🌐 Odaberi jezik"):
        st.session_state['active_module'] = "modul_0"
        st.experimental_rerun()

with cols[1]:
    if st.button("🧭 Navigacija kroz module"):
        st.session_state['active_module'] = None
        st.experimental_rerun()

with cols[2]:
    if st.button("📝 Unesi kandidata"):
        st.session_state['active_module'] = "modul_1"
        st.experimental_rerun()

with cols[0]:
    if st.button("📋 Pregled naredbi"):
        st.markdown("[📄 Preuzmi cheat sheet s naredbama](GPT_MODUL_CHEAT_SHEET.docx)")

with cols[1]:
    if st.button("📄 Primjeri CV-a"):
        st.info("⚠️ Ova funkcija još nije dostupna.")

with cols[2]:
    if st.button("🔍 Upute za korištenje"):
        st.markdown("[📘 Otvori tehničku dokumentaciju](Tehnicka_dokumentacija_GPT_MODUL_v1_2.docx)")

# MODUL NAVIGACIJA
st.markdown("### 📦 MODULI")
cols = st.columns(3)

modules = [
    ("🌍 MODUL 0", "Odabir jezika i prevoditelja", "modul_0"),
    ("🧑‍💼 MODUL 1", "Unos podataka kandidata", "modul_1"),
    ("🧹 MODUL 2", "Obrada i validacija", "modul_2"),
    ("📄 MODUL 3", "Generiranje CV-a i pisma", "modul_3"),
    ("💼 MODUL 4", "Unos podataka o oglasu", "modul_4"),
    ("📊 MODUL 5", "Analiza podudarnosti", "modul_5"),
    ("🔗 MODUL 6", "Dijeljivi link za poslodavca", "modul_6"),
    ("⭐ MODUL 7", "Evaluacija + GDPR", "modul_7"),
    ("📦 MODUL 8", "AI sažetak i arhiviranje", "modul_8")
]

for i, (title, desc, key) in enumerate(modules):
    with cols[i % 3]:
        st.subheader(title)
        st.markdown(desc)
        if st.button(f"➡️ Otvori", key=key):
            st.session_state['active_module'] = key
            st.experimental_rerun()

active = st.session_state.get('active_module', None)
if active:
    st.markdown(f"### 🔹 Aktivni modul: `{active.replace('_', ' ').title()}`")
    st.markdown("---")

# ⚙️ MODULI 0 do 8
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# MODUL 0
if active == "modul_0":
    st.header("🌍 MODUL 0: Odabir jezika i aktivacija prevoditelja")
    languages = {"Croatian": "hr", "English": "en", "German": "de", "Spanish": "es", "French": "fr"}
    lang_in = st.selectbox("Odaberi jezik unosa kandidata:", list(languages.keys()), index=0)
    lang_out = st.selectbox("Odaberi jezik za izlazne dokumente:", list(languages.keys()), index=1)
    translate_test = st.text_input("Unesi nešto za test prijevoda:")
    if translate_test:
        st.success(f"(GPT prijevod na {lang_out}): '{translate_test}'")

# MODUL 1
if active == "modul_1":
    st.header("🧑‍💼 MODUL 1: Unos podataka kandidata")
    name = st.text_input("Ime i prezime")
    email = st.text_input("Email")
    experience = st.text_area("Iskustvo (enter za novi red)")
    skills = st.text_area("Vještine (odvojene zarezima)")
    languages_spoken = st.text_area("Strani jezici")
    photo = st.file_uploader("Slika kandidata", type=["jpg", "jpeg", "png"])
    show_photo = st.radio("Prikaz slike u CV-u?", ["Da", "Ne"])
    if st.button("💾 Spremi podatke kandidata"):
        data = {
            "name": name,
            "email": email,
            "experience": experience.split("\n"),
            "skills": [s.strip() for s in skills.split(",")],
            "languages": [l.strip() for l in languages_spoken.split(",")],
            "include_photo": (show_photo == "Da"),
            "timestamp": str(datetime.now())
        }
        path = Path("data/candidate_inputs")
        path.mkdir(parents=True, exist_ok=True)
        save_json(path / f"{name.replace(' ', '_').lower()}.json", data)
        st.success("Kandidat spremljen.")

# Nastavak – MODUL 2 do MODUL 8

# MODUL 2
if active == "modul_2":
    st.header("🧹 MODUL 2: Pregled i validacija unosa kandidata")
    files = list(Path("data/candidate_inputs").glob("*.json"))
    if files:
        selected_file = st.selectbox("Odaberi kandidata", [f.name for f in files])
        data = load_json(Path("data/candidate_inputs") / selected_file)
        st.json(data)
    else:
        st.info("Nema spremljenih kandidata.")

# MODUL 3
if active == "modul_3":
    st.header("📄 MODUL 3: Generiranje životopisa i motivacijskog pisma")
    files = list(Path("data/candidate_inputs").glob("*.json"))
    if files:
        selected_file = st.selectbox("Odaberi kandidata za generiranje", [f.name for f in files])
        data = load_json(Path("data/candidate_inputs") / selected_file)
        st.subheader("📄 Životopis")
        st.markdown(f"**Ime:** {data['name']}")
        st.markdown(f"**Email:** {data['email']}")
        st.markdown("**Iskustvo:**")
        for exp in data.get("experience", []):
            st.markdown(f"- {exp}")
        st.markdown("**Vještine:** " + ", ".join(data.get("skills", [])))
        st.subheader("✉️ Motivacijsko pismo")
        st.markdown(f"Poštovani,\n\nZainteresiran sam za poziciju...\n\nS poštovanjem,\n{data['name']}")
        if st.button("✅ Spremi dokumente"):
            output = Path("outputs")
            output.mkdir(exist_ok=True)
            with open(output / f"cv_{selected_file.stem}.txt", "w") as f:
                f.write(f"CV: {json.dumps(data, indent=2)}")
            st.success("Spremljeno u 'outputs/' mapu.")
    else:
        st.info("Nema kandidata za prikaz.")

# MODUL 4
if active == "modul_4":
    st.header("💼 MODUL 4: Unos podataka o oglasu")
    job_title = st.text_input("Naziv radnog mjesta")
    company = st.text_input("Naziv tvrtke")
    location = st.text_input("Lokacija")
    deadline = st.date_input("Rok za prijavu")
    description = st.text_area("Opis posla")
    requirements = st.text_area("Zahtjevi")
    benefits = st.text_area("Benefiti")
    if st.button("💾 Spremi oglas"):
        data = {
            "job_title": job_title,
            "company": company,
            "location": location,
            "deadline": str(deadline),
            "description": description,
            "requirements": requirements,
            "benefits": benefits,
            "timestamp": str(datetime.now())
        }
        path = Path("data/job_inputs")
        path.mkdir(parents=True, exist_ok=True)
        save_json(path / f"{job_title.replace(' ', '_').lower()}.json", data)
        st.success("Oglas spremljen.")

# MODUL 5
if active == "modul_5":
    st.header("📊 MODUL 5: Analiza podudarnosti")
    cand_files = list(Path("data/candidate_inputs").glob("*.json"))
    job_files = list(Path("data/job_inputs").glob("*.json"))
    if cand_files and job_files:
        cand_name = st.selectbox("Odaberi kandidata", [f.name for f in cand_files])
        job_name = st.selectbox("Odaberi oglas", [f.name for f in job_files])
        cand = load_json(Path("data/candidate_inputs") / cand_name)
        job = load_json(Path("data/job_inputs") / job_name)
        cand_skills = set(cand.get("skills", []))
        job_reqs = set(job.get("requirements", "").split(","))
        match = cand_skills.intersection(job_reqs)
        missing = job_reqs - cand_skills
        st.markdown(f"**Podudarne vještine:** {', '.join(match)}")
        st.markdown(f"**Nedostajuće vještine:** {', '.join(missing)}")
        ratio = len(match) / max(len(job_reqs), 1) * 100
        st.success(f"📊 Podudarnost: {ratio:.1f}%")
    else:
        st.info("Unesi barem jednog kandidata i jedan oglas.")

# MODUL 6
if active == "modul_6":
    st.header("🔗 MODUL 6: Dijeljivi link za poslodavca")
    files = list(Path("data/candidate_inputs").glob("*.json"))
    if files:
        selected_file = st.selectbox("Odaberi kandidata", [f.name for f in files])
        data = load_json(Path("data/candidate_inputs") / selected_file)
        st.write("🔗 Simulirani link:")
        st.code(f"https://hr-ai.assistant/{selected_file.stem}")
        st.write("GPT refleksija:")
        st.success(f"{data['name']} pokazuje digitalnu pismenost, jasno komunicira i koristi AI alate strateški.")
    else:
        st.info("Nema kandidata.")

# MODUL 7
if active == "modul_7":
    st.header("⭐ MODUL 7: Evaluacija kandidata i poslodavca")
    candidate = st.text_input("Ime kandidata")
    employer = st.text_input("Naziv poslodavca")
    consent = st.checkbox("Kandidat je dao privolu za obradu podataka")
    rate_emp = st.slider("Ocjena poslodavca (1–5)", 1, 5, 3)
    comment_emp = st.text_area("Komentar o poslodavcu")
    rate_cand = st.slider("Ocjena kandidata (1–5)", 1, 5, 4)
    comment_cand = st.text_area("Komentar o kandidatu")
    if st.button("💾 Spremi evaluaciju"):
        data = {
            "candidate": candidate,
            "employer": employer,
            "consent": consent,
            "rate_employer": rate_emp,
            "comment_employer": comment_emp,
            "rate_candidate": rate_cand,
            "comment_candidate": comment_cand,
            "timestamp": str(datetime.now())
        }
        path = Path("data/evaluations")
        path.mkdir(parents=True, exist_ok=True)
        save_json(path / f"eval_{candidate.replace(' ', '_')}.json", data)
        st.success("Evaluacija spremljena.")

# MODUL 8
if active == "modul_8":
    st.header("📦 MODUL 8: AI sažetak i arhiviranje")
    files = list(Path("data/candidate_inputs").glob("*.json"))
    if files:
        selected_file = st.selectbox("Odaberi kandidata", [f.name for f in files])
        data = load_json(Path("data/candidate_inputs") / selected_file)
        st.subheader("📑 AI sažetak:")
        st.markdown(f"**Ime:** {data['name']}")
        st.markdown(f"**Vještine:** {', '.join(data['skills'])}")
        st.markdown(f"**Iskustvo:** {len(data['experience'])} zapisa")
        filename = st.text_input("Naziv arhive", value=f"{data['name'].replace(' ', '_')}_archived")
        if st.button("💾 Spremi u arhivu"):
            path = Path("archives")
            path.mkdir(exist_ok=True)
            save_json(path / f"{filename}.json", data)
            st.success("Prijava arhivirana.")

# app.py – Početni zaslon s jezičnim postavkama i herojskim gumbima

import streamlit as st
from datetime import datetime
import json
from pathlib import Path

st.set_page_config(page_title="GPT MODUL – Početna", layout="centered")

st.title("📊 GPT MODUL – HR AI Career Assistant v1.2")
st.caption("© 2025 Hrvoje Šajković | powered by GPT AI")

# Statusna traka za aktivni modul
active = st.session_state.get('active_module', None)
if active:
    st.markdown(f"### 🔹 Aktivni modul: `{active.replace('_', ' ').title()}`")
    st.markdown("---")

# 🌍 POSTAVKE JEZIKA – POČETNI ZASLON
st.markdown("## 🌍 Postavke jezika")
col1, col2 = st.columns(2)

with col1:
    lang_in = st.selectbox("Odaberi jezik unosa kandidata:", ["Hrvatski", "Engleski", "Njemački", "Španjolski", "Francuski"], key="lang_in")
with col2:
    lang_out = st.selectbox("Odaberi jezik za izlazne dokumente:", ["Engleski", "Njemački", "Francuski", "Hrvatski", "Španjolski"], key="lang_out")

translate_test = st.text_input("🔤 Unesi rečenicu za test prijevoda (opcionalno):")
if translate_test:
    st.info(f"🔁 (Simulirani GPT prijevod na {lang_out}): '{translate_test}'")

st.session_state["language_input"] = lang_in
st.session_state["language_output"] = lang_out

# 🎛️ HERO GUMBI
st.markdown("## 🚀 Brzi pristup")
cols = st.columns(3)

with cols[0]:
    if st.button("🧑‍💼 Unesi podatke kandidata"):
        st.session_state['active_module'] = "modul_1"
        st.experimental_rerun()

with cols[1]:
    if st.button("📄 Izradi CV i pismo"):
        st.session_state['active_module'] = "modul_3"
        st.experimental_rerun()

with cols[2]:
    if st.button("📊 Usporedi s oglasima"):
        st.session_state['active_module'] = "modul_5"
        st.experimental_rerun()

with cols[0]:
    if st.button("🔗 Prikaži link za poslodavca"):
        st.session_state['active_module'] = "modul_6"
        st.experimental_rerun()

with cols[1]:
    if st.button("📦 Arhiviraj i sažmi"):
        st.session_state['active_module'] = "modul_8"
        st.experimental_rerun()

with cols[2]:
    if st.button("🧭 Navigacija kroz sve module"):
        st.session_state['active_module'] = None
        st.experimental_rerun()

# FUNKCIJE

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# MODULI
if active == "modul_1":
    st.header("🧑‍💼 MODUL 1: Unos podataka kandidata")
    name = st.text_input("Ime i prezime")
    email = st.text_input("Email")
    experience = st.text_area("Iskustvo (enter za novi red)")
    skills = st.text_area("Vještine (odvojene zarezima)")
    languages_spoken = st.text_area("Strani jezici")
    photo = st.file_uploader("Slika kandidata", type=["jpg", "jpeg", "png"])
    show_photo = st.radio("Prikaz slike u CV-u?", ["Da", "Ne"])
    if st.button("💾 Spremi podatke kandidata"):
        data = {
            "name": name,
            "email": email,
            "experience": experience.split("\n"),
            "skills": [s.strip() for s in skills.split(",")],
            "languages": [l.strip() for l in languages_spoken.split(",")],
            "include_photo": (show_photo == "Da"),
            "timestamp": str(datetime.now())
        }
        path = Path("data/candidate_inputs")
        path.mkdir(parents=True, exist_ok=True)
        save_json(path / f"{name.replace(' ', '_').lower()}.json", data)
        st.success("Kandidat spremljen.")

if active == "modul_3":
    st.header("📄 MODUL 3: Generiranje životopisa i pisma")
    files = list(Path("data/candidate_inputs").glob("*.json"))
    if files:
        selected_file = st.selectbox("Odaberi kandidata", [f.name for f in files])
        data = load_json(Path("data/candidate_inputs") / selected_file)
        st.markdown(f"**Ime:** {data['name']}")
        st.markdown(f"**Email:** {data['email']}")
        st.markdown("**Iskustvo:**")
        for exp in data.get("experience", []):
            st.markdown(f"- {exp}")
        st.markdown("**Vještine:** " + ", ".join(data.get("skills", [])))
        st.markdown("---")
        st.markdown(f"✉️ Poštovani,\n\nZainteresiran sam za poziciju...\n\nS poštovanjem,\n{data['name']}")
        if st.button("✅ Spremi dokumente"):
            output = Path("outputs")
            output.mkdir(exist_ok=True)
            with open(output / f"cv_{selected_file.stem}.txt", "w") as f:
                f.write(f"CV: {json.dumps(data, indent=2)}")
            st.success("Spremljeno u 'outputs/' mapu.")
    else:
        st.info("Nema spremljenih kandidata.")

if active == "modul_5":
    st.header("📊 MODUL 5: Analiza podudarnosti")
    cand_files = list(Path("data/candidate_inputs").glob("*.json"))
    job_files = list(Path("data/job_inputs").glob("*.json"))
    if cand_files and job_files:
        cand_name = st.selectbox("Odaberi kandidata", [f.name for f in cand_files])
        job_name = st.selectbox("Odaberi oglas", [f.name for f in job_files])
        cand = load_json(Path("data/candidate_inputs") / cand_name)
        job = load_json(Path("data/job_inputs") / job_name)
        cand_skills = set(cand.get("skills", []))
        job_reqs = set(job.get("requirements", "").split(","))
        match = cand_skills.intersection(job_reqs)
        missing = job_reqs - cand_skills
        st.markdown(f"**Podudarne vještine:** {', '.join(match)}")
        st.markdown(f"**Nedostajuće vještine:** {', '.join(missing)}")
        ratio = len(match) / max(len(job_reqs), 1) * 100
        st.success(f"📊 Podudarnost: {ratio:.1f}%")
    else:
        st.info("Unesi barem jednog kandidata i jedan oglas.")

if active == "modul_6":
    st.header("🔗 MODUL 6: Dijeljivi link za poslodavca")
    files = list(Path("data/candidate_inputs").glob("*.json"))
    if files:
        selected_file = st.selectbox("Odaberi kandidata", [f.name for f in files])
        data = load_json(Path("data/candidate_inputs") / selected_file)
        st.code(f"https://hr-ai.assistant/{selected_file.stem}")
        st.success(f"{data['name']} pokazuje digitalnu pismenost, jasno komunicira i koristi AI alate strateški.")
    else:
        st.info("Nema kandidata.")

if active == "modul_8":
    st.header("📦 MODUL 8: AI sažetak i arhiviranje")
    files = list(Path("data/candidate_inputs").glob("*.json"))
    if files:
        selected_file = st.selectbox("Odaberi kandidata", [f.name for f in files])
        data = load_json(Path("data/candidate_inputs") / selected_file)
        st.markdown(f"**Ime:** {data['name']}")
        st.markdown(f"**Vještine:** {', '.join(data['skills'])}")
        st.markdown(f"**Iskustvo:** {len(data['experience'])} zapisa")
        filename = st.text_input("Naziv arhive", value=f"{data['name'].replace(' ', '_')}_archived")
        if st.button("💾 Spremi u arhivu"):
            path = Path("archives")
            path.mkdir(exist_ok=True)
            save_json(path / f"{filename}.json", data)
            st.success("Prijava arhivirana.")
    else:
        st.info("Nema podataka za arhiviranje.")

# ✅ Gumb za automatsko pokretanje svih inicijalnih postavki
if st.button("🟢 Pokreni sve inicijalne postavke"):
    # Postavi zadani jezik unosa i izlaza
    st.session_state["language_input"] = "Hrvatski"
    st.session_state["language_output"] = "Engleski"
    
    # Aktiviraj prvi ključni modul
    st.session_state["active_module"] = "modul_1"

    # Kreiraj sve potrebne direktorije ako ne postoje
    from pathlib import Path
    Path("data/candidate_inputs").mkdir(parents=True, exist_ok=True)
    Path("data/job_inputs").mkdir(parents=True, exist_ok=True)
    Path("outputs/cv").mkdir(parents=True, exist_ok=True)
    Path("outputs/cover_letters").mkdir(parents=True, exist_ok=True)
    Path("archives").mkdir(parents=True, exist_ok=True)
    Path("data/evaluations").mkdir(parents=True, exist_ok=True)

    # Poruka i refresh sučelja
    st.success("✅ Sustav je inicijaliziran. Modul 1 je aktiviran – spremni ste za unos kandidata.")
    st.experimental_rerun()

# MODUL_0b – Napredni jezični odabir
if st.session_state.get("active_module") == "modul_0b":
    st.header("🌍 MODUL 0b: Napredni jezični odabir")

    col1, col2 = st.columns(2)

    with col1:
        lang_in = st.selectbox("1️⃣ Odaberi jezik unosa kandidata:", [
            "Hrvatski", "Engleski", "Njemački", "Španjolski", "Francuski"
        ], key="lang_in_0b")

    with col2:
        lang_out = st.selectbox("2️⃣ Odaberi jezik izlaznih dokumenata:", [
            "Engleski", "Njemački", "Francuski", "Hrvatski", "Španjolski"
        ], key="lang_out_0b")

    lang_hr = st.radio("3️⃣ Želiš li da komunikacija prema poslodavcu (CV/pismo) bude na istom jeziku kao izlazni dokument?", ["Da", "Ne"], key="lang_same_as_output")

    if lang_hr == "Ne":
        lang_job = st.selectbox("4️⃣ Odaberi jezik komunikacije prema poslodavcu:", [
            "Engleski", "Njemački", "Francuski", "Hrvatski", "Španjolski"
        ], key="lang_job_0b")
    else:
        lang_job = lang_out

    # Spremi u session_state
    st.session_state["language_input"] = lang_in
    st.session_state["language_output"] = lang_out
    st.session_state["language_hr_doc"] = lang_job

    st.success(f"✅ Postavke spremljene:\n- Jezik unosa: {lang_in}\n- Izlazni dokumenti: {lang_out}\n- Komunikacija prema poslodavcu: {lang_job}")

# modul_9_trazenje_poslova.py

import streamlit as st
import json
from pathlib import Path
from datetime import datetime

def prikazi_modul_9():
    st.header("🔍 MODUL 9: Traženje oglasa za posao")

    # Pretpostavimo da su jezici već dohvaćeni iz CV-a
    jezici = st.session_state.get("candidate_languages", ["Engleski"])

    # Korisnik unosi pojam za traženje
    keywords = st.text_input("Koji posao tražiš? (primjer: Data Analyst)")

    # Pametna ponuda lokacija na temelju jezika
    ponude = []
    if "Engleski" in jezici:
        ponude += ["UK", "Irska", "SAD", "Remote"]
    if "Njemački" in jezici:
        ponude += ["Njemačka", "Austrija", "Švicarska"]
    if "Francuski" in jezici:
        ponude += ["Francuska", "Belgija", "Luksemburg"]
    if "Španjolski" in jezici:
        ponude += ["Španjolska", "Latinska Amerika"]
    if "Hrvatski" in jezici:
        ponude += ["Hrvatska", "SEE regija"]

    izbor = st.multiselect("Odaberi preferirane lokacije:", sorted(set(ponude)))
    custom = st.text_input("Ili upiši vlastitu lokaciju (opcionalno):")

    # Spremanje izbora u session_state
    st.session_state["job_search"] = {
        "keywords": keywords,
        "preferred_locations": izbor,
        "custom_location": custom,
        "timestamp": str(datetime.now())
    }

    if st.button("💾 Spremi kriterije pretrage"):
        path = Path("data/job_search")
        path.mkdir(parents=True, exist_ok=True)
        file_name = f"search_{keywords.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        with open(path / file_name, "w", encoding="utf-8") as f:
            json.dump(st.session_state["job_search"], f, ensure_ascii=False, indent=2)
        st.success("Kriteriji za traženje poslova spremljeni.")

# modul_9_trazenje_poslova.py

import streamlit as st
import json
from pathlib import Path
from datetime import datetime

def prikazi_modul_9():
    st.header("🔍 MODUL 9: Traženje oglasa za posao")

    jezici = st.session_state.get("candidate_languages", ["Engleski"])
    keywords = st.text_input("Koji posao tražiš? (primjer: Data Analyst)")

    ponude = []
    if "Engleski" in jezici:
        ponude += ["UK", "Irska", "SAD", "Remote"]
    if "Njemački" in jezici:
        ponude += ["Njemačka", "Austrija", "Švicarska"]
    if "Francuski" in jezici:
        ponude += ["Francuska", "Belgija", "Luksemburg"]
    if "Španjolski" in jezici:
        ponude += ["Španjolska", "Latinska Amerika"]
    if "Hrvatski" in jezici:
        ponude += ["Hrvatska", "SEE regija"]

    izbor = st.multiselect("Odaberi preferirane lokacije:", sorted(set(ponude)))
    custom = st.text_input("Ili upiši vlastitu lokaciju (opcionalno):")

    st.session_state["job_search"] = {
        "keywords": keywords,
        "preferred_locations": izbor,
        "custom_location": custom,
        "timestamp": str(datetime.now())
    }

    if st.button("💾 Spremi kriterije pretrage"):
        path = Path("data/job_search")
        path.mkdir(parents=True, exist_ok=True)
        file_name = f"search_{keywords.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        with open(path / file_name, "w", encoding="utf-8") as f:
            json.dump(st.session_state["job_search"], f, ensure_ascii=False, indent=2)
        st.success("Kriteriji za traženje poslova spremljeni.")

    # Učitavanje izvora
    st.subheader("🌐 Relevantni izvori za traženje poslova")
    sources_path = Path("/mnt/data/job_sources_database.json")
    if sources_path.exists():
        with open(sources_path, "r", encoding="utf-8") as f:
            all_sources = json.load(f)

        for lokacija in izbor:
            country = lokacija.split(" ")[0]  # pojednostavljena pretpostavka
            if country in all_sources:
                st.markdown(f"**{country}**")
                for url in all_sources[country]["sources"]:
                    st.markdown(f"- [🔗 {url}]({url})")
    else:
        st.warning("Izvori poslova nisu pronađeni.")

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

# MODUL 9 – Traženje poslova s prikazom portala
if active == "modul_9":
    st.header("🔍 MODUL 9: Traženje poslova")

    cand_files = list(Path("data/candidate_inputs").glob("*.json"))
    if cand_files:
        selected_file = st.selectbox("Odaberi kandidata", [f.name for f in cand_files])
        data = load_json(Path("data/candidate_inputs") / selected_file)

        experience = " ".join(data.get("experience", []))
        skills = ", ".join(data.get("skills", []))
        auto_keywords = f"{skills}, {experience}"

        st.markdown("### ✏️ Unesi detalje za traženje poslova")
        keywords = st.text_area("🔑 Ključne riječi (AI generirano, možeš urediti)", value=auto_keywords)
        locations = st.multiselect("📍 Lokacije za pretragu", ["Zagreb", "Remote", "Beč", "Bruxelles", "Frankfurt", "Amsterdam", "Ljubljana", "Prag"], default=["Zagreb"])
        languages = data.get("languages", [])

        if st.button("💾 Spremi kriterije i prikaži portale"):
            search_data = {
                "keywords": keywords,
                "preferred_locations": locations,
                "languages": languages,
                "timestamp": str(datetime.now())
            }
            output_dir = Path("data/job_search")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"search_{selected_file.stem}.json"
            save_json(output_file, search_data)
            st.success(f"Kriteriji spremljeni kao {output_file.name}")

            st.markdown("### 🌐 Preporučeni portali po lokaciji:")
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

            for loc in locations:
                if loc in portal_links:
                    st.markdown(f"**{loc}:**")
                    for name, url in portal_links[loc]:
                        st.markdown(f"- [{name}]({url})")
    else:
        st.info("Nema spremljenih kandidata.")
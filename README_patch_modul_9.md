# ✅ Upute za korištenje zakrpe `patch_modul_9.diff`

Ova zakrpa dodaje **MODUL 9 – Traženje poslova** u vaš `app.py` bez ručnog prepisivanja postojećeg koda.

---

## 🛠️ Što sadrži zakrpa:
- Dodaje gumb **“🔍 Traženje poslova”** u početni izbornik
- Poziva funkciju `prikazi_modul_9()` unutar `render_module()`
- Pretpostavlja da postoji datoteka `modul_9_trazenje_poslova.py` s tom funkcijom

---

## 📁 Lokacija
Preporučuje se pohrana u:
```
/patches/patch_modul_9.diff
```

---

## 💻 Kako primijeniti zakrpu

U terminalu pokrenite:
```bash
patch app.py < patches/patch_modul_9.diff
```

Ako zakrpa uspješno prođe, dobit ćete poruku poput:
```
patching file app.py
```

---

## 🔎 Napomena
Zakrpa se može ručno pregledati ili primijeniti u editoru. Idealna je za verzijske sustave (npr. Git).


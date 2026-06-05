import streamlit as st
import urllib.request, json
st.set_page_config(page_title="Dharura AI — Maandalizi ya Dharura", page_icon="🆘", layout="centered")
st.markdown("""<style>.stApp{background:#0a0000;color:#ffebee}
.d-card{background:#1a0000;border:1px solid #b71c1c;border-radius:10px;padding:14px 18px;margin:8px 0}
.green-card{background:#0a1f0d;border:1px solid #1b5e20;border-radius:10px;padding:14px 18px;margin:8px 0}
.stButton>button{background:#b71c1c;color:#fff;border:none;border-radius:8px;padding:10px 24px;font-weight:700;width:100%}
</style>""", unsafe_allow_html=True)
SYS = "Wewe ni mshauri wa dharura na uokoaji Kenya. Toa habari za wazi za kuokoa maisha kwa Kiswahili. Kama kuna hatari ya papo hapo, toa nambari za dharura kwanza kabla ya kitu kingine chochote."
API_KEY = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY","")

# ── Public-facing service availability check ──────────────────────────────────
if not API_KEY:
    st.warning(
        "⚠️ **Huduma hii haipo tayari katika toleo hili la majaribio.**\n\n"
        "Tunaendelea kuboresha. Rudi baadaye au wasiliana na msimamizi.\n\n"
        "_This service is not yet available in this demo version. "
        "We are working on it — please check back soon._"
    )
    st.stop()

def ask(q):
    if not API_KEY: return "❌ API key not configured."
    url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    body={"contents":[{"role":"user","parts":[{"text":q}]}],"systemInstruction":{"parts":[{"text":SYS}]},"generationConfig":{"temperature":0.1,"maxOutputTokens":600}}
    try:
        req=urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r: return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e: return f"❌ {e}"
st.markdown("# 🆘 Dharura AI"); st.markdown("**Maandalizi ya Dharura Kenya**")
st.markdown('<div class="d-card">🚨 NAMBARI ZA DHARURA:<br>🔴 Polisi: 999 / 0800 722 203<br>🚒 Zima Moto: 020 222 2181<br>🏥 Ambulance: 1199 / 0800 723 253<br>🌊 NDMA Floods: 020 271 4099</div>',unsafe_allow_html=True)
tab1,tab2,tab3=st.tabs(["🌊 Mafuriko","🔥 Moto","🏥 Msaada wa Kwanza"])
with tab1:
    county=st.selectbox("Kaunti yako:",["Nairobi","Kisumu","Tana River","Turkana","Garissa","Mombasa","Nakuru"])
    if st.button("🌊 Hatua za Dharura ya Mafuriko",key="f1"):
        with st.spinner("..."): r=ask(f"Dharura ya mafuriko katika {county} Kenya. Hatua za mara moja: nini cha kufanya, wapi kukimbia, na jinsi ya kupata msaada wa NDMA. Orodhesha vituo vya kukusanyika.")
        st.markdown(f'<div class="d-card">{r.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
with tab2:
    fire_type=st.selectbox("Aina ya moto:",["Moto wa nyumba","Moto wa ghorofa","Moto wa msitu","Moto wa gari"])
    if st.button("🔥 Hatua za Dharura ya Moto",key="f2"):
        with st.spinner("..."): r=ask(f"Dharura ya {fire_type} Kenya. Hatua za mara moja, jinsi ya kukimbia salama, na jinsi ya kupiga simu Zima Moto. Habari za kuokoa maisha kwanza.")
        st.markdown(f'<div class="d-card">{r.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
with tab3:
    aid_type=st.selectbox("Hali:",["Mtu amezimia","Jeraha kubwa/kutoka damu","Mshtuko wa moyo","Mtoto amemeza kitu","Sumu/ulevi wa kemikali"])
    if st.button("🏥 Msaada wa Kwanza",key="f3"):
        with st.spinner("..."): r=ask(f"Msaada wa kwanza kwa {aid_type}. Hatua 1-2-3 za haraka kabla daktari hawajafika. Ni lini kupiga simu 1199.")
        st.markdown(f'<div class="green-card">{r.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
st.markdown("---"); st.caption("🆘 Dharura AI v1.0 | NDMA: ndma.go.ke | KRC: redcross.or.ke | Polisi: 999 | CC BY-NC-ND 4.0")

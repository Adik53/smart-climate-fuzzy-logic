import streamlit as st
import pandas as pd
import numpy as np
from fuzzy_system import SmartClimateSystem
import visualizations as vis

st.set_page_config(
    page_title="Bulanık Mantık İklim Kontrolü",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def sistem_yukle():
    return SmartClimateSystem()


f_sys = sistem_yukle()

st.markdown("""
<style>
.main {background-color: #f8f9fa;}
.metric-box {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.07);
    border-left: 5px solid #4CAF50;
    margin-bottom: 4px;
}
.interpreter-text {
    font-size: 1.15rem;
    font-weight: bold;
    color: #1E3A8A;
}
</style>
""", unsafe_allow_html=True)

st.title("🌡️ Bulanık Mantık ile Akıllı İklimlendirme Kontrol Sistemi")
st.markdown(
    "Bu sistem, odanın anlık **sıcaklık**, **nem** ve **boyut** parametrelerini analiz ederek "
    "ideal fan hızını bulanık mantık kuralları ile belirler."
)

st.sidebar.header("Adilet Kairzhanov 217039921")
st.sidebar.header("🎛️ Sistem Kontrol Paneli")

hazir_senaryolar = {
    "Özel Ayarlar": None,
    "Sıcak Yaz Günü (Büyük Salon)": {"T": 36, "H": 85, "S": 55},
    "Ilık Sonbahar (Küçük Oda)":    {"T": 21, "H": 50, "S": 12},
    "Kuru ve Soğuk Gün":            {"T": 8,  "H": 25, "S": 30},
    "Nemli ve Tropikal Ortam":      {"T": 29, "H": 90, "S": 45},  # ← DÜZELTİLDİ
}

secilen_senaryo = st.sidebar.selectbox(
    "📋 Hazır Senaryo Seçimi", list(hazir_senaryolar.keys())
)

if secilen_senaryo != "Özel Ayarlar":
    veriler = hazir_senaryolar[secilen_senaryo]
    varsayilan_t = veriler["T"]
    varsayilan_h = veriler["H"]
    varsayilan_s = veriler["S"]
else:
    varsayilan_t = 24
    varsayilan_h = 50
    varsayilan_s = 25

T_input = st.sidebar.slider("🌡️ Sıcaklık (°C)",       0, 40,  varsayilan_t,
                             help="Oda sıcaklığı (0–40 °C)")
H_input = st.sidebar.slider("💧 Nem (%)",              0, 100, varsayilan_h,
                             help="Odadaki bağıl nem oranı")
S_input = st.sidebar.slider("📐 Oda Boyutu (m²)",      0, 100, varsayilan_s,
                             help="İklimlendirilecek alanın büyüklüğü (0–100 m²)")

hesaplanan_hiz, aktif_kurallar = f_sys.hesapla(T_input, H_input, S_input)
klasik_hiz = f_sys.klasik_kontrol_karsilastir(T_input, H_input, S_input)
yorum = f_sys.linguistik_yorum(hesaplanan_hiz)
fark  = hesaplanan_hiz - klasik_hiz

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-box">
        <p style='margin:0;color:#666;font-size:.9rem;'>Bulanık Hesaplanan Fan Hızı</p>
        <h2 style='margin:4px 0 0;'>%{hesaplanan_hiz:.2f}</h2>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-box" style="border-left-color:#007BFF;">
        <p style='margin:0;color:#666;font-size:.9rem;'>Klasik Kontrol Çıktısı</p>
        <h2 style='margin:4px 0 0;'>%{klasik_hiz:.2f}</h2>
    </div>""", unsafe_allow_html=True)
with col3:
    isaretli = f"+{fark:.2f}" if fark >= 0 else f"{fark:.2f}"
    renk = "#E57373" if fark > 0 else "#81C784"
    st.markdown(f"""
    <div class="metric-box" style="border-left-color:{renk};">
        <p style='margin:0;color:#666;font-size:.9rem;'>Fark (Bulanık − Klasik)</p>
        <h2 style='margin:4px 0 0;color:{renk};'>{isaretli}%</h2>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-box" style="border-left-color:#FFC107;">
        <p style='margin:0;color:#666;font-size:.9rem;'>Sistem Modu</p>
        <p class="interpreter-text" style='margin:4px 0 0;'>{yorum}</p>
    </div>""", unsafe_allow_html=True)

st.write("")

sekme1, sekme2, sekme3, sekme4 = st.tabs([
    "📈 Üyelik Fonks. & Durulama",
    "🧮 Kural Tabanı & Ateşlenmeler",
    "🧪 Kontrol Yüzeyi Analizi",
    "📊 Test Raporu & Dışa Aktarım",
])

with sekme1:
    st.header("Sistem Fonksiyonları ve Durulama Görselleştirmesi")

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.pyplot(vis.uylik_fonksiyonu_ciz(
            f_sys.sicaklik, "Sıcaklık Üyelik Fonksiyonları", "Sıcaklık (°C)"))
        st.pyplot(vis.uylik_fonksiyonu_ciz(
            f_sys.oda_boyutu, "Oda Boyutu Üyelik Fonksiyonları", "Alan (m²)"))
    with col_g2:
        st.pyplot(vis.uylik_fonksiyonu_ciz(
            f_sys.nem, "Nem Üyelik Fonksiyonları", "Nem (%)"))
        st.pyplot(vis.uylik_fonksiyonu_ciz(
            f_sys.fan_hizi, "Fan Hızı Çıktı Üyelik Fonksiyonları", "Fan Gücü (%)"))

    st.markdown("---")
    st.subheader("Bulanık Çıkarım Sonucu Ağırlık Merkezi (Centroid)")
    st.pyplot(vis.durulama_gorsellestir(f_sys, hesaplanan_hiz))

with sekme2:
    st.header("Çıkarım Mekanizması Kural Analizi")

    col_r1, col_r2 = st.columns([6, 4])
    with col_r1:
        st.subheader(f"Aktif Kurallar ({len(aktif_kurallar)} adet)")
        if aktif_kurallar:
            for kural in aktif_kurallar:
                pct = int(kural['ateslenme_gucu'] * 100)
                renk = "#E57373" if pct > 60 else ("#FFC107" if pct > 30 else "#81C784")
                st.markdown(
                    f"<div style='padding:8px 12px;margin-bottom:6px;border-radius:6px;"
                    f"border-left:4px solid {renk};background:#fff;'>"
                    f"<b>Kural {kural['id']}:</b> {kural['kural_metni']}"
                    f"<span style='float:right;font-weight:bold;color:{renk};'>"
                    f"{kural['ateslenme_gucu']:.3f}</span></div>",
                    unsafe_allow_html=True
                )
        else:
            st.warning("Bu girdi kombinasyonu için hiçbir kural ateşlenmedi.")

    with col_r2:
        st.subheader("Aktivasyon Dağılımı")
        st.pyplot(vis.kural_aktivasyon_grafigi(aktif_kurallar))

with sekme3:
    st.header("Hassasiyet ve Kontrol Yüzeyi Analizi")

    oda_sabit = st.slider("Sabit Oda Boyutu (m²)", 0, 100, 30,
                          help="3D yüzey ve ısı haritası için sabit tutulan değer")

    col_3d, col_2d = st.columns([3, 2])
    with col_3d:
        st.markdown("**3D Kontrol Yüzeyi**")
        with st.spinner("Yüzey hesaplanıyor..."):
            st.pyplot(vis.kontrol_yuzeyi_3d(f_sys, oda_boyutu_sabit=oda_sabit))
    with col_2d:
        st.markdown("**2D Isı Haritası**")
        with st.spinner("Isı haritası hesaplanıyor..."):
            st.pyplot(vis.sicaklik_nem_isı_haritasi(f_sys, oda_boyutu_sabit=oda_sabit))

with sekme4:
    st.header("Performans Test Verileri ve Raporlama")

    test_verileri_ham = [
        (15, 40, 20), (25, 60, 35), (35, 80, 55),
        (38, 20, 15), (10, 90, 45),
    ]
    rows = []
    for t, h, s in test_verileri_ham:
        hz, _ = f_sys.hesapla(t, h, s)
        kl    = f_sys.klasik_kontrol_karsilastir(t, h, s)
        rows.append({
            "Sıcaklık (°C)": t,
            "Nem (%)": h,
            "Oda Boyutu (m²)": s,
            "Bulanık Fan Hızı (%)": round(hz, 1),
            "Klasik Fan Hızı (%)": round(kl, 1),
            "Fark (%)": round(hz - kl, 1),
        })

    df_test = pd.DataFrame(rows)
    st.dataframe(df_test, use_container_width=True)

    st.markdown("---")
    st.subheader("Mevcut Anlık Veriyi Kaydet")

    anlik_veri = pd.DataFrame([{
        "Sıcaklık (°C)": T_input,
        "Nem (%)": H_input,
        "Oda Boyutu (m²)": S_input,
        "Hesaplanan Fan Hızı (%)": f"{hesaplanan_hiz:.2f}",
        "Klasik Kontrol Hızı (%)": f"{klasik_hiz:.2f}",
        "Fark (%)": f"{fark:.2f}",
        "Sistem Yorumu": yorum,
        "Aktif Kural Sayısı": len(aktif_kurallar),
    }])

    csv = anlik_veri.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Analiz Sonuçlarını CSV Olarak İndir",
        data=csv,
        file_name='akilli_iklimlendirme_analiz_raporu.csv',
        mime='text/csv',
    )
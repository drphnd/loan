import streamlit as st
import pandas as pd
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Sistem Penilaian Kredit",
    page_icon="🇮🇩",
    layout="wide",
    initial_sidebar_state="collapsed" # Sidebar ditutup agar fokus
)

# --- SESSION STATE (NAVIGASI) ---
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'dashboard'

def navigate_to(page):
    st.session_state['current_page'] = page
    st.rerun()

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    h1, h2, h3 { font-family: 'Segoe UI', sans-serif; color: #0f172a; font-weight: 600; }
    .stMarkdown p { color: #334155; font-size: 1.05rem; }
    
    div[data-testid="stExpander"] { border: 1px solid #e2e8f0; border-radius: 8px; background-color: #f8fafc; }
    
    /* Tombol Utama */
    .stButton button {
        background-color: #0f172a;
        color: white;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        border: none;
        width: 100%;
        transition: all 0.2s;
    }
    .stButton button:hover {
        background-color: #334155;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Tombol Back */
    div[data-testid="stButton"] button[kind="secondary"] {
        background-color: transparent;
        color: #64748b;
        border: 1px solid #cbd5e1;
    }
    div[data-testid="stButton"] button[kind="secondary"]:hover {
        background-color: #f1f5f9;
        color: #0f172a;
    }
</style>
""", unsafe_allow_html=True)

# --- KONSTANTA MATA UANG (IDR) ---
CURS_SYMBOL = "Rp"
EXCHANGE_RATE = 16000 # Asumsi kurs untuk normalisasi ke model (1 USD = 16.000 IDR)

# ==============================================================================
# HALAMAN 1: DASHBOARD
# ==============================================================================
if st.session_state['current_page'] == 'dashboard':
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Sistem Penilaian Risiko Kredit")
        st.markdown(f"""
        Sistem pendukung keputusan kredit berbasis data untuk **Indonesia**. 
        Menggunakan analisis parameter finansial untuk mengestimasi risiko peminjam secara objektif.
        
        **Mata Uang Operasional:** Indonesian Rupiah (IDR)
        """)
        
        st.write("") 
        # Tombol Navigasi ke Halaman Analisis
        st.button("Buat Analisis Baru ➜", on_click=navigate_to, args=('analysis',))

    with col2:
        # Metrik Ringkasan
        st.metric("Total Aplikasi", "1,240", "+5%")
        st.metric("Rata-rata Approval", "72%", "-1.5%")

# ==============================================================================
# HALAMAN 2: ANALISIS (FORM & HASIL)
# ==============================================================================
elif st.session_state['current_page'] == 'analysis':
    
    # Tombol Back
    col_back, col_title = st.columns([1, 10])
    with col_back:
        st.write("") 
        if st.button("← Kembali"):
            navigate_to('dashboard')
            
    with col_title:
        st.title("Formulir Pengajuan Kredit")

    st.markdown("Lengkapi data pemohon di bawah ini. Semua nilai dalam **Rupiah (Rp)**.")
    
    # --- FORM INPUT ---
    with st.container():
        col_left, col_right = st.columns(2, gap="large")
        
        # Input Data Pemohon
        with col_left:
            st.subheader("Profil Pemohon")
            with st.expander("Data Pribadi & Pekerjaan", expanded=True):
                annual_inc = st.number_input(
                    f"Pendapatan Tahunan ({CURS_SYMBOL})", 
                    min_value=0, 
                    value=120000000, # Default 120 Juta/Tahun (Gaji 10jt/bulan)
                    step=5000000,
                    format="%d",
                    help="Total gaji kotor dalam setahun (Gaji bulanan x 12)"
                )
                home_ownership = st.selectbox("Status Rumah", ["MORTGAGE (KPR)", "OWN (Milik Sendiri)", "RENT (Sewa)", "OTHER"])
                emp_length = st.selectbox("Lama Bekerja", ["< 1 tahun", "1-3 tahun", "4-7 tahun", "8-10 tahun", "10+ tahun"])
        
        # Input Data Pinjaman
        with col_right:
            st.subheader("Parameter Pinjaman")
            with st.expander("Detail Finansial", expanded=True):
                loan_amount = st.number_input(
                    f"Jumlah Pinjaman ({CURS_SYMBOL})", 
                    min_value=0, 
                    value=50000000, # Default 50 Juta
                    step=1000000,
                    format="%d"
                )
                col_sub1, col_sub2 = st.columns(2)
                with col_sub1: term = st.selectbox("Tenor", ["36 Bulan", "60 Bulan"])
                with col_sub2: int_rate = st.number_input("Suku Bunga (%)", 0.0, 30.0, 11.5, step=0.1)
                dti = st.number_input("DTI Ratio (%)", 0.0, 100.0, 18.0, step=0.1, help="Debt-to-Income Ratio (Rasio Hutang terhadap Pendapatan)")

    st.markdown("---")
    analyze_btn = st.button("Hitung Risiko Kredit")

    # --- LOGIKA KALKULASI ---
    if analyze_btn:
        with st.spinner('Sedang menganalisis profil risiko...'):
            time.sleep(1) # Simulasi loading
            
            # 1. NORMALISASI KE USD (Agar logika model konsisten)
            # Input user (IDR) dibagi kurs (16.000)
            inc_usd = annual_inc / EXCHANGE_RATE
            loan_usd = loan_amount / EXCHANGE_RATE
            
            # 2. ALGORITMA SCORING (SIMULASI SENSITIF)
            # Faktor 1: DTI & Bunga
            risk_score = (dti * 0.6) + (int_rate * 0.3)
            
            # Faktor 2: Rasio Pinjaman terhadap Gaji
            # Jika pinjaman terlalu besar dibanding gaji tahunan, risiko naik
            if inc_usd > 0:
                loan_to_income = loan_usd / inc_usd
                risk_score += (loan_to_income * 20)
            
            # Faktor 3: Bonus Profil
            if "OWN" in home_ownership or "MORTGAGE" in home_ownership: 
                risk_score -= 5
            if emp_length in ["8-10 tahun", "10+ tahun"]: 
                risk_score -= 3
            
            # Normalisasi skor 0-100
            risk_score = max(0, min(risk_score, 100))
            prob_default = risk_score / 100
            
            # 3. HITUNG LIMIT AMAN (DALAM IDR)
            monthly_inc = annual_inc / 12
            max_installment = monthly_inc * 0.35 # Max cicilan aman: 35% gaji
            
            r = (int_rate / 100) / 12
            n = 36 if "36" in term else 60
            
            # Max pinjaman berdasarkan cicilan aman
            max_loan_limit = max_installment * (1 - (1 + r)**(-n)) / r
            
            # 4. KEPUTUSAN AKHIR
            # Disetujui jika risiko rendah (<50%) DAN pinjaman tidak melebihi 120% limit aman
            is_approved = (prob_default < 0.5) and (loan_amount <= max_loan_limit * 1.2)

        # --- HASIL ANALISIS ---
        st.subheader("Hasil Analisis")
        r_col1, r_col2 = st.columns([1, 3])
        
        with r_col1:
            final_score = int(100 - risk_score)
            st.metric("Skor Kredit", f"{final_score}/100", 
                     delta="Risiko Rendah" if final_score > 60 else "Risiko Tinggi",
                     delta_color="normal" if final_score > 60 else "inverse")
        
        with r_col2:
            # Format Rupiah
            formatted_limit = f"{CURS_SYMBOL} {int(max_loan_limit):,}".replace(",", ".")
            formatted_loan = f"{CURS_SYMBOL} {int(loan_amount):,}".replace(",", ".")
            
            if is_approved:
                if loan_amount <= max_loan_limit:
                    st.success("✅ **REKOMENDASI: DISETUJUI**")
                    st.write("Profil risiko pemohon rendah dan kapasitas pembayaran mencukupi.")
                    st.markdown(f"**Jumlah Disetujui:** {formatted_loan}")
                else:
                    st.warning("⚠️ **REKOMENDASI: DISETUJUI SEBAGIAN (TURUN PLAFON)**")
                    st.write("Profil risiko bagus, namun jumlah pengajuan melebihi kapasitas cicilan aman.")
                    st.markdown(f"**Limit Disarankan:** {formatted_limit}")
                
            else:
                st.error("❌ **REKOMENDASI: DITOLAK**")
                st.write(f"Risiko gagal bayar terlalu tinggi (Probabilitas: {prob_default:.1%}) atau beban utang berlebihan.")
import streamlit as strl
import google.generativeai as genai

# Konfigurasi kunci API Gemini dari Secrets Streamlit
try:
    genai.configure(api_key=strl.secrets["GEMINI_API_KEY"])
except Exception:
    strl.error("API Key Gemini belum diatur di Advanced Settings -> Secrets!")

# Konfigurasi Halaman Utama Aplikasi
strl.set_page_config(page_title="MusicCip", page_icon="🎵", layout="centered")

strl.title("🎵 MusicCip")
strl.caption("AI Pembuat Musik, Not Angka & Chord Otomatis")
strl.write("Selamat datang di MusicCip! Ciptakan lirik lagu, not angka, dan chord gitar instan dengan bantuan kecerdasan buatan.")

# Membuat Menu Navigasi Tab
tab1, tab2 = strl.tabs(["🔍 Analisis & Bedah Musik", "✍️ Ciptakan Lagu Baru"])

# ==========================================
# MENU 1: ANALISIS & BEDAH MUSIK
# ==========================================
with tab1:
    strl.header("🔍 Analisis Komposisi Musik")
    strl.write("Masukkan lirik atau struktur lagu untuk dianalisis progresi chord dan maknanya.")
    
    input_musik = strl.text_area("Tempel lirik atau progresi chord di sini:", height=150, placeholder="Contoh: C - G - Am - F...")
    tombol_analisis = strl.button("Bedah Musik Sekarang", key="btn_analisis")
    
    if tombol_analisis:
        if input_musik.strip() == "":
            strl.warning("Silakan masukkan teks musik terlebih dahulu!")
        else:
            with strl.spinner("AI sedang membedah struktur musikmu..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    perintah = f"Analisis struktur musik, progresi chord, dan makna dari teks musik berikut secara mendalam namun mudah dipahami: {input_musik}"
                    respons = model.generate_content(perintah)
                    strl.success("Analisis Selesai!")
                    strl.markdown(respons.text)
                except Exception as e:
                    strl.error(f"Terjadi kesalahan saat menghubungi AI: {e}")

# ==========================================
# MENU 2: CIPTAKAN LAGU BARU
# ==========================================
with tab2:
    strl.header("✍️ Generator Lagu & Not Angka")
    strl.write("Tentukan tema, genre, dan biarkan AI menulis lagu lengkap untukmu.")
    
    tema = strl.text_input("Apa tema lagu yang diinginkan?", placeholder="Contoh: Rindu kampung halaman, persahabatan, patah hati...")
    genre = strl.selectbox("Pilih Genre Musik:", ["Pop", "Akustik / Folk", "Dangdut", "Rock", "Jazz", "Reggae"])
    tempo = strl.select_slider("Pilih Tempo Lagu:", options=["Lambat (Slow)", "Sedang (Moderate)", "Cepat (Fast)"])
    
    tombol_cipta = strl.button("Ciptakan Lagu Sekarang", key="btn_cipta")
    
    if tombol_cipta:
        if tema.strip() == "":
            strl.warning("Silakan isi tema lagu terlebih dahulu!")
        else:
            with strl.spinner("AI sedang menggubah lirik, not angka, dan chord untukmu..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    perintah = (
                        f"Buatkan sebuah lagu utuh (ada Bait/Verse dan Reff/Chorus) dengan tema '{tema}', "
                        f"bergenre {genre}, dengan tempo {tempo}. "
                        f"PENTING: Tuliskan chord gitarnya di atas lirik secara presisi, "
                        f"dan sertakan juga panduan 'Not Angka' (1 2 3 4 5 6 7) di setiap baris liriknya "
                        f"agar lagu ini bisa langsung dinyanyikan atau dimainkan dengan alat musik."
                    )
                    respons = model.generate_content(perintah)
                    strl.success("Lagu Berhasil Diciptakan!")
                    strl.markdown(respons.text)
                except Exception as e:
                    strl.error(f"Terjadi kesalahan saat menghubungi AI: {e}")

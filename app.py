import streamlit as st
import google.generativeai as genai

# 1. KONFIGURASI AI GEMINI & HALAMAN UTAMA
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="MusicCip - AI Pembuat Musik, Not & Chord", page_icon="🎵", layout="centered")

# Tampilan Atas Aplikasi
st.title("🎵 MusicCip")
st.subheader("Platform AI Kreator Musik, Lirik, & Chord Otomatis")
st.write("Selamat datang di MusicCip! Gunakan menu di bawah ini untuk menciptakan musik atau menulis lagu baru lengkap dengan not angka dan kunci gitar.")

# MEMBUAT DUA MENU TAB (NAVIGASI)
tab1, tab2 = st.tabs(["🎸 Ciptakan Musik dari Lirik", "📝 Buat Lirik + Not & Chord Otomatis"])

# ==========================================
# MENU 1: CIPTAKAN MUSIK DARI LIRIK
# ==========================================
with tab1:
    st.header("Ciptakan Musik Otomatis")
    lirik_input = st.text_area("✍️ Masukkan Lirik Lagu Anda:", height=150, placeholder="Tempel lirik lagu di sini...", key="lirik_main")
    
    genre_pilihan = st.selectbox(
        "🎸 Pilih Gaya Musik Utama:", 
        ["Otomatis (Deteksi Emosi Lirik oleh AI)", "Pop Modern", "Rock Bersemangat", "Jazz Santai", "Akustik Syahdu", "Dangdut Asik"],
        key="genre_box"
    )

    if st.button("MULAI CIPTAKAN MUSIK 🚀", key="btn_music"):
        if lirik_input:
            with st.spinner("🔮 MusicCip sedang merancang aransemen musik..."):
                if genre_pilihan == "Otomatis (Deteksi Emosi Lirik oleh AI)":
                    prompt_analisis = f"Analisis lirik lagu ini: '{lirik_input}'. Tentukan genre musik, mood, dan perkiraan tempo (BPM). Jawab singkat 1 paragraf."
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    respons = model.generate_content(prompt_analisis)
                    st.info(f"**📋 Hasil Analisis Otomatis AI:**\n{respons.text}")
                else:
                    st.info(f"Aransemen disiapkan untuk Gaya: {genre_pilihan}")
                
                st.warning("🔄 Menghubungkan ke server audio generator...")
                st.success("🎉 Musik berhasil dibuat! (Fitur audio .mp3 sedang disiapkan)")
        else:
            st.warning("Silakan masukkan lirik lagunya terlebih dahulu!")

# ==========================================
# MENU 2: BUAT LIRIK + NOT ANGKA & CHORD OTOMATIS
# ==========================================
with tab2:
    st.header("Asisten Penulis Lagu, Not Angka & Chord")
    st.write("Tulis ide cerita atau tema lagu yang Anda inginkan. AI akan membuatkan lirik lengkap beserta panduan nada menggunakan not angka dan kunci gitar (chord)!")
    
    tema_input = st.text_input("💡 Masukkan Tema / Ide Lagu Anda:", placeholder="Contoh: Lagu ceria tentang keindahan desa, atau lagu sedih tentang perpisahan")
    
    if st.button("GENERATE LIRIK, NOT & CHORD 📝✨", key="btn_lyrics"):
        if tema_input:
            with st.spinner("✍️ MusicCip sedang menggubah lirik, not angka, dan kunci gitar..."):
                
                # Prompt baru yang memerintahkan Gemini membuat lirik, not angka, dan chord gitar secara sejajar
                prompt_songwriter = f"""
                Buatlah sebuah lirik lagu utuh yang memiliki nada dan harmonisasi indah berdasarkan tema ini: '{tema_input}'. 
                Lagu harus terdiri dari struktur standar: Bait 1 (Verse 1), Bait 2 (Verse 2), Reff (Chorus), dan Penutup (Outro).
                
                STRUKTUR PENULISAN SETIAP BARIS LAGU WAJIB SEPERTI INI:
                Tuliskan baris KUNCI GITAR/CHORD (seperti C, G, Am, F, Dm, dll) di baris paling atas.
                Tuliskan baris NOT ANGKA (menggunakan angka 1 2 3 4 5 6 7, titik, dan garis ketukan) di baris kedua.
                Tuliskan baris LIRIK LAGU tepat di bawahnya agar posisi ketukan chord, not angka, dan liriknya SEJAJAR dan pas saat dimainkan.
                
                Contoh format tampilan yang wajib Anda ikuti:
                [Bait 1]
                Chord:      C           F           G           C
                Not Angka:  3  .  4  |  5  .  1  |  7  .  6  |  5  .
                Lirik:      Ha  ri    i     ni    ku    ba    ha  gia
                """
                
               model = genai.GenerativeModel('gemini-1.5-flash')
                respons = model.generate_content(prompt_songwriter)
                
                st.success("✨ Lagu, Not Angka & Chord Berhasil Diciptakan!")
                st.markdown("---")
                # Menggunakan st.code agar format spasi/jarak antarteks terjaga rapi dan tidak bergeser di layar HP
                st.code(respons.text, language="text")
                st.markdown("---")
                st.caption("Tips: Anda bisa menyalin teks di atas untuk disimpan atau langsung dimainkan dengan gitar/piano Anda!")
        else:
            st.warning("Silakan isi tema atau ide lagunya terlebih dahulu!")

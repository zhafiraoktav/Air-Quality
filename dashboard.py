import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Custom CSS
st.markdown(
    """
    <style>
    body {
        background-color: #C8A2C8; /* Warna lilac untuk background */
    }
    h1 {
        color: #4B0082; /* Warna ungu tua untuk title */
    }
    h2 {
        color: #9932CC; /* Warna medium orchid untuk subheader */
    }
    h3 {
        color: #8A2BE2; /* Warna biru violet untuk subheader kecil */
    }
    .plot-container {
        border: 2px solid #4B0082; /* Warna border */
        padding: 10px; /* Ruang di dalam border */
        border-radius: 5px; /* Sudut border yang melengkung */
        margin-bottom: 20px; /* Jarak bawah dari elemen lain */
        background-color: #FFFFFF; /* Warna background untuk container */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Membaca file CSV
df = pd.read_csv('kualitas_udara.csv')

# Menampilkan judul utama aplikasi
st.title("Air Quality Dashboard Across Stations")

# Menampilkan header
st.header("Air Pollution Data Analysis Across Stations")

# Membuat filter dropdown berdasarkan polutan
pollutant_option = st.selectbox(
    'Select the pollutant to analyze:',
    ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
)

# Menampilkan grafik sesuai pilihan pengguna
st.subheader(f'Average {pollutant_option} per Year at Aotizhongxin Station')

# Cek apakah kolom 'year' dan 'station' sudah ada
if 'year' in df.columns and 'station' in df.columns and pollutant_option in df.columns:
    # Filter data untuk stasiun yang dipilih
    df_filtered = df[df['station'] == 'Aotizhongxin']

    # Filter data berdasarkan polutan yang dipilih
    df_filtered_pollutant = df_filtered[['year', pollutant_option]]

    # Mengelompokkan berdasarkan 'year', lalu menghitung rata-rata untuk polutan yang dipilih
    df_grouped = df_filtered_pollutant.groupby('year')[pollutant_option].mean().reset_index()

    # Lihat hasil df_grouped
    st.write(f"Pollutant data (Average per Year for {pollutant_option}):", df_grouped)

    # Membuat plot dengan Matplotlib - Line Plot untuk Rata-Rata Tahunan
    plt.figure(figsize=(7, 4))
    plt.plot(df_grouped['year'], df_grouped[pollutant_option], marker='o', label=pollutant_option)
    plt.title(f'Average {pollutant_option} per Year')
    plt.xlabel('Year')
    plt.ylabel(f'Average {pollutant_option} Concentration')
    plt.xticks(df_grouped['year'])
    plt.grid()
    plt.legend()
    st.pyplot(plt)

    # Membuat plot dengan Matplotlib - Bar Chart untuk Rata-Rata Tahunan
    plt.figure(figsize=(7, 4))
    plt.bar(df_grouped['year'], df_grouped[pollutant_option], label=pollutant_option, alpha=0.5, color='#4B0082')  # Warna ungu
    plt.title(f'Average {pollutant_option} per Year (Bar Chart)')
    plt.xlabel('Year')
    plt.ylabel(f'Average {pollutant_option} Concentration')
    plt.xticks(df_grouped['year'])
    plt.grid()
    plt.legend()
    st.pyplot(plt)

else:
    st.error("Kolom 'year', 'station', atau polutan yang dipilih tidak ditemukan.")

# Pilih stasiun untuk dianalisis
station_option = st.selectbox(
    'Select the station to analyze:',
    ['Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan', 'Gucheng', 'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong']
)

st.subheader(f'Average Pollutant Levels at {station_option} Station per Year')

# Cek apakah kolom 'year' dan 'station' sudah ada
if 'year' in df.columns and 'station' in df.columns:
    # Filter data untuk stasiun yang dipilih
    df_filtered = df[df['station'] == station_option]

    # Pilih hanya kolom numerik yang relevan
    numeric_columns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    
    # Mengelompokkan berdasarkan 'year', lalu menghitung rata-rata
    df_grouped = df_filtered.groupby('year')[numeric_columns].mean().reset_index()

    # Lihat hasil df_grouped
    st.write(f"Average pollutant data at {station_option} station:", df_grouped)

    # Membuat plot dengan Matplotlib - Line Plot untuk Rata-Rata Tahunan
    plt.figure(figsize=(10, 5))
    for col in numeric_columns:
        plt.plot(df_grouped['year'], df_grouped[col], marker='o', label=col)
    plt.title(f'Average Pollutants at {station_option} per Year')
    plt.xlabel('Year')
    plt.ylabel('Average Concentration (µg/m³)')
    plt.xticks(df_grouped['year'])
    plt.grid()
    plt.legend()
    st.pyplot(plt)

# Menghitung korelasi antara kelembaban (DEWP), suhu (TEMP), PM2.5, dan PM10
if all(col in df.columns for col in ['DEWP', 'TEMP', 'PM2.5', 'PM10']):
    correlation_matrix = df[['DEWP', 'TEMP', 'PM2.5', 'PM10']].corr()
    
    # Tampilkan korelasi dalam Streamlit
    st.subheader("Correlation Between Dew Point, Temperature, PM2.5, and PM10")
    st.write(correlation_matrix)

    # Visualisasikan heatmap untuk korelasi
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Matrix Correlation Between Dew Point, Temperature, PM2.5, and PM10')
    st.pyplot(plt)
else:
    st.error("Kolom yang diperlukan untuk menghitung korelasi tidak ditemukan.")

# Rata-rata konsentrasi polutan per stasiun
if 'station' in df.columns:
    average_Polutan = df.groupby('station')[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean()

    # Visualisasi tabel rata-rata konsentrasi polutan di posisi tengah
    st.subheader("Average Pollutant Concentrations Across Various Stations")
    st.write(average_Polutan.style.set_properties(**{'text-align': 'center'}))

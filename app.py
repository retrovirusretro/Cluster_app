import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import io

# Sayfa ayarları
st.set_page_config(page_title="Cluster App", layout="wide")
st.title("🔍 K-Means Cluster Analizi")

# Kullanıcıdan dosya yüklemesini iste
uploaded_file = st.file_uploader("Lütfen 'Cluster_Data.xlsm' dosyasını yükleyin", type=["xlsm"])

if uploaded_file:
    # Excel dosyasını oku
    xls = pd.ExcelFile(uploaded_file)

    # Ortak metrikler
    metrics = [
        "GMROI",
        "Stok Devir Hızı",
        "Satış Tutar",
        "Rate Of Sales (Haftalık Ağırlıklı)",
        "Satış Kar Oranı",
        "Ciro Pay",
        "M2",
        "Satış Miktar"
    ]

    # Etiketler
    cluster_labels = {0: 'LXX', 1: 'LX', 2: 'L', 3: 'M', 4: 'S', 5: 'SX'}

    def cluster_dataframe(df, key_cols, level_name):
        df['Key'] = df[key_cols].agg(" | ".join, axis=1)
        for metric in metrics:
            results = []
            for key, group in df.groupby('Key'):
                group = group.copy()
                if len(group) > 2:
                    kmeans = KMeans(n_clusters=3, random_state=42)
                    group[f'{metric} Cluster'] = kmeans.fit_predict(group[[metric]])
                    cluster_order = group.groupby(f'{metric} Cluster')[metric].mean().sort_values().index
                    if metric == "Stok Devir Hızı":
                        cluster_map = {cluster_order[i]: i + 2 for i in range(len(cluster_order))}
                    else:
                        cluster_map = {cluster_order[i]: 4 - i for i in range(len(cluster_order))}
                    group[f'{metric} Cluster'] = group[f'{metric} Cluster'].map(cluster_map)
                    if metric == "Stok Devir Hızı":
                        group.loc[group[metric] < group[metric].quantile(0.05), f'{metric} Cluster'] = 5
                        group.loc[group[metric] > group[metric].quantile(0.95), f'{metric} Cluster'] = 1
                    else:
                        group.loc[group[metric] > group[metric].quantile(0.95), f'{metric} Cluster'] = 1
                        group.loc[group[metric] < group[metric].quantile(0.05), f'{metric} Cluster'] = 5
                else:
                    group[f'{metric} Cluster'] = 'N/A'
                results.append(group)
            df = pd.concat(results)

        for column in [f"{metric} Cluster" for metric in metrics]:
            df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
            df[column] = df[column].map(cluster_labels)
        return df

    # AltKategori
    df_alt = pd.read_excel(xls, sheet_name="AltKategori", header=6)
    df_alt = cluster_dataframe(df_alt, ["AileAdı", "KategoriAdı", "AltKategoriAdı"], "AltKategori")

    # Kategori
    df_cat = pd.read_excel(xls, sheet_name="Kategori", header=6)
    df_cat = cluster_dataframe(df_cat, ["AileAdı", "KategoriAdı"], "Kategori")

    # Aile
    df_aile = pd.read_excel(xls, sheet_name="Aile", header=6)
    df_aile = cluster_dataframe(df_aile, ["AileAdı"], "Aile")

    # Excel çıktısı
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_alt.to_excel(writer, sheet_name="AltKategori Cluster", index=False)
        df_cat.to_excel(writer, sheet_name="Kategori Cluster", index=False)
        df_aile.to_excel(writer, sheet_name="Aile Cluster", index=False)
    output.seek(0)

    st.success("✅ Analiz tamamlandı! Aşağıdan çıktıyı indirebilirsiniz.")
    st.download_button(
        label="📥 Excel Sonucunu İndir",
        data=output,
        file_name="Cluster_Analizi_Sonuç.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

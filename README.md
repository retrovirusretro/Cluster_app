# 📊 Cluster App – K-Means Kümeleme Uygulaması

Bu uygulama, `Aile`, `Kategori` ve `AltKategori` düzeyinde satış metriklerini kullanarak KMeans algoritması ile ürünleri sınıflandırır. Çıktılar, etiketlenmiş ve kolay okunabilir şekilde Excel dosyası olarak sunulur.

## 🚀 Nasıl Kullanılır?

1. Bu repo'yu klonlayın:
```bash
git clone https://github.com/kullaniciadi/cluster-app.git
cd cluster-app
```

2. Ortamı kurun:
```bash
pip install -r requirements.txt
```

3. Streamlit uygulamasını başlatın:
```bash
streamlit run app.py
```

4. Uygulamada `Cluster_Data.xlsm` dosyasını yükleyin ve çıktıyı indirin.

## 📁 Girdi Dosyası Formatı
- Excel dosyasında şu sayfalar yer almalı:
  - `AltKategori` (7. satırdan itibaren veri başlar)
  - `Kategori` (7. satırdan itibaren veri başlar)
  - `Aile` (7. satırdan itibaren veri başlar)

## 📦 Gerekli Kütüphaneler
- streamlit
- pandas
- scikit-learn
- openpyxl
- xlsxwriter

## 🛠️ Geliştirici Notu
Metrikler ve etiket sistemi ihtiyaca göre kolayca özelleştirilebilir.

---

🎉 İyi analizler!

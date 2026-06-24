# 🌡️ Bulanık Mantık ile Akıllı İklimlendirme Kontrol Sistemi

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-fuzzy](https://img.shields.io/badge/scikit--fuzzy-0.4.2-4CAF50?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Sıcaklık, nem ve oda boyutunu gerçek zamanlı analiz ederek fan hızını otomatik belirleyen, bulanık mantık tabanlı akıllı iklimlendirme sistemi.**

[Kurulum](#-kurulum) • [Nasıl Çalışır](#-nasıl-çalışır) • [Özellikler](#-özellikler) • [Ekran Görüntüleri](#-ekran-görüntüleri) • [Mimari](#-proje-mimarisi)

</div>

---

## 📋 İçindekiler

- [Proje Hakkında](#-proje-hakkında)
- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Nasıl Çalışır](#-nasıl-çalışır)
  - [Giriş Değişkenleri](#giriş-değişkenleri)
  - [Üyelik Fonksiyonları](#üyelik-fonksiyonları)
  - [Kural Tabanı](#kural-tabanı)
  - [Durulama](#durulama-defuzzification)
- [Arayüz Sekmeleri](#-arayüz-sekmeleri)
- [Hazır Senaryolar](#-hazır-senaryolar)
- [Klasik Kontrol ile Karşılaştırma](#-klasik-kontrol-ile-karşılaştırma)
- [Bağımlılıklar](#-bağımlılıklar)
- [Geliştirici](#-geliştirici)

---

## 🎯 Proje Hakkında

Bu proje, **Bulanık Mantık (Fuzzy Logic)** yöntemini kullanarak bir odanın iklimlendirme sistemini akıllı biçimde kontrol etmeyi amaçlamaktadır. Geleneksel on/off veya sabit eşik tabanlı sistemlerin aksine, bulanık mantık sayesinde sistem belirsiz ve sürekli değişen ortam koşullarına yumuşak, gerçekçi ve enerji verimli tepkiler üretebilmektedir.

Sistem üç temel giriş parametresi alır:

| Parametre | Aralık | Açıklama |
|---|---|---|
| 🌡️ **Sıcaklık** | 0 – 40 °C | Odanın anlık sıcaklık ölçümü |
| 💧 **Nem** | 0 – 100 % | Odadaki bağıl nem oranı |
| 📐 **Oda Boyutu** | 0 – 100 m² | İklimlendirilecek alanın büyüklüğü |

Ve tek bir çıkış üretir:

| Çıkış | Aralık | Açıklama |
|---|---|---|
| 🌀 **Fan Hızı** | 0 – 100 % | Hesaplanan optimum fan çalışma hızı |

---

## ✨ Özellikler

- 🧠 **Mamdani Tipi Bulanık Çıkarım** — 27 kurallı tam kapsam kural tabanı
- 📊 **Gerçek Zamanlı Görselleştirme** — Üyelik fonksiyonları, aktivasyon grafikleri, defuzzification analizi
- 🗺️ **3D Kontrol Yüzeyi** — Sıcaklık × Nem → Fan Hızı ilişkisinin üç boyutlu görünümü
- 🔥 **2D Isı Haritası** — Kontrol yüzeyinin alternatif, kolay okunur gösterimi
- ⚖️ **Klasik Kontrol Karşılaştırması** — Bulanık ve eşik tabanlı sistemlerin yan yana analizi
- 📋 **Hazır Senaryo Yönetimi** — 4 farklı gerçek dünya senaryosu ile hızlı test
- 🏷️ **Dilsel Yorum** — Fan hızı çıktısının insan okunabilir durum etiketine dönüştürülmesi
- 📥 **CSV Raporlama** — Anlık analiz sonuçlarını dışa aktarma

---

## 🚀 Kurulum

### Gereksinimler

- Python **3.9** veya üzeri
- pip paket yöneticisi

### Adım Adım

**1. Depoyu klonlayın**

```bash
git clone https://github.com/kullanici-adi/akilli-iklimlendirme.git
cd akilli-iklimlendirme
```

**2. Sanal ortam oluşturun (önerilir)**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Bağımlılıkları yükleyin**

```bash
pip install -r requirements.txt
```

**4. Uygulamayı başlatın**

```bash
streamlit run app.py
```

Tarayıcınızda otomatik olarak `http://localhost:8501` açılacaktır.

---

## 📦 Bağımlılıklar

```txt
streamlit>=1.28.0
numpy>=1.24.0
scikit-fuzzy>=0.4.2
matplotlib>=3.7.0
seaborn>=0.12.0
pandas>=2.0.0
networkx>=3.0
```

`requirements.txt` oluşturmak için:

```bash
pip freeze > requirements.txt
```

---

## 💻 Kullanım

Uygulama açıldığında sol kenar çubuğundan üç parametre ayarlanabilir:

```
Sıcaklık   [────●──────────] 24 °C
Nem        [──────●─────────] 50 %
Oda Boyutu [────●──────────] 25 m²
```

Sliderlar hareket ettirildiğinde sistem anında yeniden hesaplama yapar ve tüm grafikler güncellenir.

Hızlı test için **hazır senaryolar** açılır menüsünden seçim yapılabilir.

---

## 🧠 Nasıl Çalışır

Sistem klasik **Mamdani Bulanık Çıkarım** mimarisini izler:

```
Crisp Girdiler → Bulanıklaştırma → Kural Değerlendirme → Küme Birleştirme → Durulama → Crisp Çıktı
     (T, H, S)    (Fuzzification)    (Rule Evaluation)    (Aggregation)   (Defuzz.)    (fan_hizi)
```

### Giriş Değişkenleri

Her giriş değişkeni üç dilsel terime ayrılmıştır:

```
Sıcaklık  →  Düşük  |  Orta  |  Yüksek
Nem       →  Kuru   |  Normal |  Nemli
Oda Boy.  →  Küçük  |  Orta   |  Büyük
```

Çıkış değişkeni:

```
Fan Hızı  →  Yavaş  |  Orta  |  Hızlı
```

### Üyelik Fonksiyonları

Trapez (`trapmf`) ve üçgen (`trimf`) fonksiyonları kullanılmıştır:

**Sıcaklık:**

```
μ
1 ┤████▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  │     Düşük       Orta        Yüksek
0 └──┬──────┬────────┬──────────┬──────── °C
   0        12  15  22  25  30  32        40
```

| Terim | Fonksiyon | Parametreler |
|-------|-----------|--------------|
| Düşük | trapmf | [0, 0, 12, 22] |
| Orta | trimf | [15, 22, 30] |
| Yüksek | trapmf | [25, 32, 40, 40] |

**Nem:**

| Terim | Fonksiyon | Parametreler |
|-------|-----------|--------------|
| Kuru | trapmf | [0, 0, 30, 50] |
| Normal | trimf | [40, 55, 70] |
| Nemli | trapmf | [60, 75, 100, 100] |

**Oda Boyutu:**

| Terim | Fonksiyon | Parametreler |
|-------|-----------|--------------|
| Küçük | trapmf | [0, 0, 20, 40] |
| Orta | trimf | [30, 50, 70] |
| Büyük | trapmf | [60, 80, 100, 100] |

**Fan Hızı (Çıkış):**

| Terim | Fonksiyon | Parametreler |
|-------|-----------|--------------|
| Yavaş | trapmf | [0, 0, 20, 45] |
| Orta | trimf | [35, 50, 65] |
| Hızlı | trapmf | [55, 80, 100, 100] |

### Kural Tabanı

Sistem 3 × 3 × 3 = **27 kural** içermektedir. Tüm kombinasyonlar eksiksiz kapsanmaktadır:

| # | Sıcaklık | Nem | Oda | → Fan Hızı |
|---|----------|-----|-----|-----------|
| 1 | Düşük | Kuru | Küçük | **Yavaş** |
| 2 | Düşük | Normal | Küçük | **Yavaş** |
| 3 | Düşük | Nemli | Küçük | **Orta** |
| 4 | Düşük | Kuru | Orta | **Yavaş** |
| 5 | Düşük | Normal | Orta | **Yavaş** |
| 6 | Düşük | Nemli | Orta | **Orta** |
| 7 | Düşük | Kuru | Büyük | **Yavaş** |
| 8 | Düşük | Normal | Büyük | **Orta** |
| 9 | Düşük | Nemli | Büyük | **Orta** |
| 10 | Orta | Kuru | Küçük | **Yavaş** |
| 11 | Orta | Normal | Küçük | **Orta** |
| 12 | Orta | Nemli | Küçük | **Orta** |
| 13 | Orta | Kuru | Orta | **Orta** |
| 14 | Orta | Normal | Orta | **Orta** |
| 15 | Orta | Nemli | Orta | **Hızlı** |
| 16 | Orta | Kuru | Büyük | **Orta** |
| 17 | Orta | Normal | Büyük | **Hızlı** |
| 18 | Orta | Nemli | Büyük | **Hızlı** |
| 19 | Yüksek | Kuru | Küçük | **Orta** |
| 20 | Yüksek | Normal | Küçük | **Hızlı** |
| 21 | Yüksek | Nemli | Küçük | **Hızlı** |
| 22 | Yüksek | Kuru | Orta | **Hızlı** |
| 23 | Yüksek | Normal | Orta | **Hızlı** |
| 24 | Yüksek | Nemli | Orta | **Hızlı** |
| 25 | Yüksek | Kuru | Büyük | **Hızlı** |
| 26 | Yüksek | Normal | Büyük | **Hızlı** |
| 27 | Yüksek | Nemli | Büyük | **Hızlı** |

> **AND** operatörü için minimum (min) yöntemi kullanılmaktadır.

### Durulama (Defuzzification)

Birleştirilmiş çıkış kümesinin **ağırlık merkezi (centroid)** yöntemi ile tek bir crisp değere dönüştürülmesi:

```
         ∫ x · μ_agg(x) dx
y* =  ─────────────────────
           ∫ μ_agg(x) dx
```

Bu yöntem, tüm aktif kuralların katkısını dengeli biçimde yansıtır ve sürekli, pürüzsüz bir kontrol çıktısı üretir.

---

### Veri Akışı

```
┌─────────────────────────────────────────────────────┐
│                      app.py                          │
│  Sidebar Sliders → T, H, S                          │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│                  fuzzy_system.py                     │
│                                                     │
│  hesapla(T, H, S)                                   │
│  ├── clip(T, 0, 40), clip(H, 0, 100), clip(S, 0, 100)│
│  ├── simulator.compute()  → fan_hizi (crisp)         │
│  └── _aktif_kurallari_bul() → [kural listesi]        │
│                                                     │
│  klasik_kontrol_karsilastir(T, H, S) → klasik_hiz   │
│  linguistik_yorum(fan_hizi) → "🟡 Orta Yük"         │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│                 visualizations.py                    │
│  • Üyelik fonksiyonu grafikleri                     │
│  • Defuzzification görselleştirmesi                 │
│  • Kural aktivasyon çubuk grafiği                   │
│  • 3D kontrol yüzeyi + 2D ısı haritası              │
└─────────────────────────────────────────────────────┘
```

---

## 📑 Arayüz Sekmeleri

### 📈 Sekme 1 — Üyelik Fonksiyonları & Durulama

Dört üyelik fonksiyonu grafiği (Sıcaklık, Nem, Oda Boyutu, Fan Hızı) ve mevcut girdiler için defuzzification analizini içerir. Centroid değeri mor dikey çizgi ile gösterilir.

### 🧮 Sekme 2 — Kural Tabanı & Ateşlenmeler

Mevcut girdiler için hangi kuralların aktif olduğunu, her kuralın ateşlenme gücünü ve çıktı terimini renkli göstergelerle listeler. Yatay çubuk grafiği ile aktivasyon dağılımını görselleştirir.

### 🧪 Sekme 3 — Kontrol Yüzeyi Analizi

Sabit oda boyutu için Sıcaklık × Nem → Fan Hızı ilişkisini hem 3D yüzey hem de 2D ısı haritası olarak gösterir. Sekmedeki slider ile sabit oda boyutu değiştirilebilir.

### 📊 Sekme 4 — Test Raporu & Dışa Aktarım

Beş farklı test senaryosunu dinamik olarak hesaplar ve bulanık/klasik sistemleri karşılaştırır. Anlık analiz sonuçlarını CSV formatında indirme imkânı sunar.

---

## 🎭 Hazır Senaryolar

| Senaryo | Sıcaklık | Nem | Oda | Beklenen Çıktı |
|---------|----------|-----|-----|----------------|
| 🌞 Sıcak Yaz Günü (Büyük Salon) | 36 °C | 85% | 55 m² | Hızlı (~85%) |
| 🍂 Ilık Sonbahar (Küçük Oda) | 21 °C | 50% | 12 m² | Yavaş (~25%) |
| ❄️ Kuru ve Soğuk Gün | 8 °C | 25% | 30 m² | Yavaş (~10%) |
| 🌴 Nemli ve Tropikal Ortam | 29 °C | 90% | 45 m² | Hızlı (~75%) |

---

## ⚖️ Klasik Kontrol ile Karşılaştırma

Sistem, eşik tabanlı geleneksel kontrol yaklaşımıyla sürekli karşılaştırma yapar:

| Özellik | Bulanık Mantık | Klasik Kontrol |
|---------|---------------|----------------|
| Geçiş bölgeleri | Yumuşak, sürekli | Keskin, ani |
| Belirsizlik toleransı | ✅ Yüksek | ❌ Düşük |
| Kural sayısı | 27 (tam kapsam) | 3 eşik |
| Enerji verimliliği | ✅ Optimize | ⚠️ Aşırı/yetersiz |
| Yorumlanabilirlik | ✅ Dilsel | ⚠️ Sayısal |

---

## 🏷️ Sistem Durumu Etiketleri

Hesaplanan fan hızına göre sistem otomatik olarak durum etiketi üretir:

```
Fan Hızı  0–30%  →  🟢 Düşük Yük — Konforlu
Fan Hızı 30–55%  →  🟡 Orta Yük  — Normal
Fan Hızı 55–75%  →  🟠 Yüksek Yük — Yoğun
Fan Hızı 75–100% →  🔴 Maksimum Yük — Kritik
```

---

## Geliştirici

**Adilet Kairzhanov**
Öğrenci No: 217039921

---

## 📄 Lisans

Bu proje MIT lisansı ile lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.

---

<div align="center">

Bulanık Mantık · scikit-fuzzy · Streamlit · Python

</div>

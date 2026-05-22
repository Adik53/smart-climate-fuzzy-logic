import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import skfuzzy as fuzz

sns.set_theme(style="whitegrid", context="talk")

def uylik_fonksiyonu_ciz(antecedent_or_consequent, baslik, etiket_x):
    fig, ax = plt.subplots(figsize=(10, 4))
    for terim in antecedent_or_consequent.terms:
        ax.plot(antecedent_or_consequent.universe, 
                antecedent_or_consequent[terim].mf, 
                linewidth=2.5, 
                label=terim)
    ax.set_title(baslik, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(etiket_x, fontsize=12)
    ax.set_ylabel("Üyelik Derecesi (μ)", fontsize=12)
    ax.legend(loc='upper right', frameon=True)
    ax.set_ylim(-0.05, 1.05)
    plt.tight_layout()
    return fig

def durulama_gorsellestir(system, hesaplanarak_bulunan_hiz):
    universe = system.fan_hizi.universe
    yavas_mf = system.fan_hizi['Yavas'].mf
    orta_mf = system.fan_hizi['Orta'].mf
    hizli_mf = system.fan_hizi['Hizli'].mf
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.fill_between(universe, 0, yavas_mf, facecolor='blue', alpha=0.15, label='Yavaş')
    ax.fill_between(universe, 0, orta_mf, facecolor='green', alpha=0.15, label='Orta')
    ax.fill_between(universe, 0, hizli_mf, facecolor='red', alpha=0.15, label='Hızlı')
    
    ax.plot(universe, yavas_mf, 'b', linewidth=1, linestyle='--')
    ax.plot(universe, orta_mf, 'g', linewidth=1, linestyle='--')
    ax.plot(universe, hizli_mf, 'r', linewidth=1, linestyle='--')
    
    ax.axvline(hesaplanarak_bulunan_hiz, color='purple', linewidth=3, 
               label=f'Ağırlık Merkezi (Centroid): {hesaplanarak_bulunan_hiz:.2f}%')
    
    ax.set_title("Durulama (Defuzzification) Analizi ve Çıktı Kümesi", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Fan Hızı (%)", fontsize=12)
    ax.set_ylabel("Üyelik Derecesi (μ)", fontsize=12)
    ax.legend(loc='upper left', frameon=True)
    ax.set_ylim(-0.05, 1.05)
    plt.tight_layout()
    return fig

def kural_aktivasyon_grafigi(aktif_kurallar):
    if not aktif_kurallar:
        fig, ax = plt.subplots(figsize=(6, 2))
        ax.text(0.5, 0.5, "Aktif Kural Bulunmamaktadır", ha='center', va='center')
        ax.axis('off')
        return fig
        
    ids = [f"Kural {k['id']}" for k in aktif_kurallar]
    gcler = [k['ateslenme_gucu'] for k in aktif_kurallar]
    
    fig, ax = plt.subplots(figsize=(10, max(3, len(ids) * 0.5)))
    colors = sns.color_palette("viridis", len(ids))
    bars = ax.barh(ids, gcler, color=colors, edgecolor='grey', height=0.6)
    
    ax.set_xlabel("Ateşlenme Gücü (Aktivasyon Seviyesi)", fontsize=12)
    ax.set_title("Kuralların Aktivasyon Seviyeleri Analizi", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlim(0, 1.05)
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.01, bar.get_y() + bar.get_height()/2, f'{width:.2f}', 
                va='center', ha='left', fontsize=11, fontweight='bold')
                
    plt.tight_layout()
    return fig

def kontrol_yuzeyi_3d(system):
    x = np.linspace(0, 40, 20)
    y = np.linspace(0, 100, 20)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros(X.shape)
    
    for i in range(20):
        for j in range(20):
            system.simulator.input['sicaklik'] = X[i, j]
            system.simulator.input['nem'] = Y[i, j]
            system.simulator.input['oda_boyutu'] = 30
            try:
                system.simulator.compute()
                Z[i, j] = system.simulator.output['fan_hizi']
            except:
                Z[i, j] = 0
                
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', edgecolor='none', alpha=0.9)
    
    ax.set_xlabel('Sıcaklık (°C)', fontsize=11)
    ax.set_ylabel('Nem (%)', fontsize=11)
    ax.set_zlabel('Fan Hızı (%)', fontsize=11)
    
    ax.xaxis.labelpad = 10
    ax.yaxis.labelpad = 10
    ax.zaxis.labelpad = 10
    
    ax.set_title('Kontrol Yüzeyi (Oda Boyutu = 30 m² sabitken)', fontsize=14, fontweight='bold', pad=20)
    fig.colorbar(surf, shrink=0.5, aspect=10, pad=0.1)
    plt.tight_layout()
    return fig
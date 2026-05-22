import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class SmartClimateSystem:
    def __init__(self):
        self.sicaklik = ctrl.Antecedent(np.arange(0, 41, 1), 'sicaklik')
        self.nem = ctrl.Antecedent(np.arange(0, 101, 1), 'nem')
        self.oda_boyutu = ctrl.Antecedent(np.arange(0, 101, 1), 'oda_boyutu')
        self.fan_hizi = ctrl.Consequent(np.arange(0, 101, 1), 'fan_hizi')

        self._uyelik_fonksiyonlarini_olustur()
        self._kural_tabanini_olustur()

    def _uyelik_fonksiyonlarini_olustur(self):
        self.sicaklik['Dusuk'] = fuzz.trapmf(self.sicaklik.universe, [0, 0, 12, 22])
        self.sicaklik['Orta']  = fuzz.trimf(self.sicaklik.universe,  [15, 22, 30])
        self.sicaklik['Yuksek'] = fuzz.trapmf(self.sicaklik.universe, [25, 32, 40, 40])

        self.nem['Kuru']   = fuzz.trapmf(self.nem.universe, [0, 0, 30, 50])
        self.nem['Normal'] = fuzz.trimf(self.nem.universe,  [40, 55, 70])
        self.nem['Nemli']  = fuzz.trapmf(self.nem.universe, [60, 75, 100, 100])

        self.oda_boyutu['Kucuk'] = fuzz.trapmf(self.oda_boyutu.universe, [0, 0, 20, 40])
        self.oda_boyutu['Orta']  = fuzz.trimf(self.oda_boyutu.universe,  [30, 50, 70])
        self.oda_boyutu['Buyuk'] = fuzz.trapmf(self.oda_boyutu.universe, [60, 80, 100, 100])

        self.fan_hizi['Yavas'] = fuzz.trapmf(self.fan_hizi.universe, [0, 0, 20, 45])
        self.fan_hizi['Orta']  = fuzz.trimf(self.fan_hizi.universe,  [35, 50, 65])
        self.fan_hizi['Hizli'] = fuzz.trapmf(self.fan_hizi.universe, [55, 80, 100, 100])

    def _kural_tabanini_olustur(self):
        s = self.sicaklik
        n = self.nem
        b = self.oda_boyutu
        f = self.fan_hizi

        self.kurallar = [
            # Dusuk 
            ctrl.Rule(s['Dusuk'] & n['Kuru']   & b['Kucuk'], f['Yavas']),
            ctrl.Rule(s['Dusuk'] & n['Normal'] & b['Kucuk'], f['Yavas']),
            ctrl.Rule(s['Dusuk'] & n['Nemli']  & b['Kucuk'], f['Orta']),
            ctrl.Rule(s['Dusuk'] & n['Kuru']   & b['Orta'],  f['Yavas']),
            ctrl.Rule(s['Dusuk'] & n['Normal'] & b['Orta'],  f['Yavas']),
            ctrl.Rule(s['Dusuk'] & n['Nemli']  & b['Orta'],  f['Orta']),
            ctrl.Rule(s['Dusuk'] & n['Kuru']   & b['Buyuk'], f['Yavas']),
            ctrl.Rule(s['Dusuk'] & n['Normal'] & b['Buyuk'], f['Orta']),
            ctrl.Rule(s['Dusuk'] & n['Nemli']  & b['Buyuk'], f['Orta']),
            # Orta
            ctrl.Rule(s['Orta'] & n['Kuru']   & b['Kucuk'], f['Yavas']),
            ctrl.Rule(s['Orta'] & n['Normal'] & b['Kucuk'], f['Orta']),
            ctrl.Rule(s['Orta'] & n['Nemli']  & b['Kucuk'], f['Orta']),
            ctrl.Rule(s['Orta'] & n['Kuru']   & b['Orta'],  f['Orta']),
            ctrl.Rule(s['Orta'] & n['Normal'] & b['Orta'],  f['Orta']),
            ctrl.Rule(s['Orta'] & n['Nemli']  & b['Orta'],  f['Hizli']),
            ctrl.Rule(s['Orta'] & n['Kuru']   & b['Buyuk'], f['Orta']),
            ctrl.Rule(s['Orta'] & n['Normal'] & b['Buyuk'], f['Hizli']),
            ctrl.Rule(s['Orta'] & n['Nemli']  & b['Buyuk'], f['Hizli']),
            # Yuksek
            ctrl.Rule(s['Yuksek'] & n['Kuru']   & b['Kucuk'], f['Orta']),
            ctrl.Rule(s['Yuksek'] & n['Normal'] & b['Kucuk'], f['Hizli']),
            ctrl.Rule(s['Yuksek'] & n['Nemli']  & b['Kucuk'], f['Hizli']),
            ctrl.Rule(s['Yuksek'] & n['Kuru']   & b['Orta'],  f['Hizli']),
            ctrl.Rule(s['Yuksek'] & n['Normal'] & b['Orta'],  f['Hizli']),
            ctrl.Rule(s['Yuksek'] & n['Nemli']  & b['Orta'],  f['Hizli']),
            ctrl.Rule(s['Yuksek'] & n['Kuru']   & b['Buyuk'], f['Hizli']),
            ctrl.Rule(s['Yuksek'] & n['Normal'] & b['Buyuk'], f['Hizli']),
            ctrl.Rule(s['Yuksek'] & n['Nemli']  & b['Buyuk'], f['Hizli']),
        ]

        self.kontrol_sistemi = ctrl.ControlSystem(self.kurallar)
        self.simulator = ctrl.ControlSystemSimulation(self.kontrol_sistemi)

    def hesapla(self, T: float, H: float, S: float):
        """
        Parametreler
        ------------
        T : Sıcaklık (0-40 °C)
        H : Nem     (0-100 %)
        S : Oda boyutu (0-100 m²)

        Döndürür
        --------
        (cikti_hizi, aktif_kurallar)
        """
        T = float(np.clip(T, 0, 40))
        H = float(np.clip(H, 0, 100))
        S = float(np.clip(S, 0, 100))

        self.simulator.input['sicaklik']  = T
        self.simulator.input['nem']       = H
        self.simulator.input['oda_boyutu'] = S

        try:
            self.simulator.compute()
            cikti_hizi = float(self.simulator.output['fan_hizi'])
        except Exception as e:
            cikti_hizi = 0.0

        aktif_kurallar = self._aktif_kurallari_bul(T, H, S)

        return cikti_hizi, aktif_kurallar

    def _aktif_kurallari_bul(self, T: float, H: float, S: float) -> list:
        """
        Her kuralın ateşlenme gücünü min() operatörü ile elle hesapla.
        Bu yöntem skfuzzy'nin iç API değişikliklerinden bağımsızdır.
        """
        s_u = self.sicaklik.universe
        n_u = self.nem.universe
        b_u = self.oda_boyutu.universe

        s_deg = {
            t: float(fuzz.interp_membership(s_u, self.sicaklik[t].mf, T))
            for t in ('Dusuk', 'Orta', 'Yuksek')
        }
        n_deg = {
            t: float(fuzz.interp_membership(n_u, self.nem[t].mf, H))
            for t in ('Kuru', 'Normal', 'Nemli')
        }
        b_deg = {
            t: float(fuzz.interp_membership(b_u, self.oda_boyutu[t].mf, S))
            for t in ('Kucuk', 'Orta', 'Buyuk')
        }

        kural_tanimlari = [
            ('Dusuk','Kuru','Kucuk','Yavas'), ('Dusuk','Normal','Kucuk','Yavas'),
            ('Dusuk','Nemli','Kucuk','Orta'),  ('Dusuk','Kuru','Orta','Yavas'),
            ('Dusuk','Normal','Orta','Yavas'), ('Dusuk','Nemli','Orta','Orta'),
            ('Dusuk','Kuru','Buyuk','Yavas'),  ('Dusuk','Normal','Buyuk','Orta'),
            ('Dusuk','Nemli','Buyuk','Orta'),

            ('Orta','Kuru','Kucuk','Yavas'),  ('Orta','Normal','Kucuk','Orta'),
            ('Orta','Nemli','Kucuk','Orta'),  ('Orta','Kuru','Orta','Orta'),
            ('Orta','Normal','Orta','Orta'),  ('Orta','Nemli','Orta','Hizli'),
            ('Orta','Kuru','Buyuk','Orta'),   ('Orta','Normal','Buyuk','Hizli'),
            ('Orta','Nemli','Buyuk','Hizli'),

            ('Yuksek','Kuru','Kucuk','Orta'),  ('Yuksek','Normal','Kucuk','Hizli'),
            ('Yuksek','Nemli','Kucuk','Hizli'),('Yuksek','Kuru','Orta','Hizli'),
            ('Yuksek','Normal','Orta','Hizli'),('Yuksek','Nemli','Orta','Hizli'),
            ('Yuksek','Kuru','Buyuk','Hizli'), ('Yuksek','Normal','Buyuk','Hizli'),
            ('Yuksek','Nemli','Buyuk','Hizli'),
        ]

        aktif = []
        for i, (st, nt, bt, ft) in enumerate(kural_tanimlari):
            derece = min(s_deg[st], n_deg[nt], b_deg[bt])
            if derece > 1e-6:
                aktif.append({
                    'id': i + 1,
                    'kural_metni': f"EĞER Sıcaklık={st} VE Nem={nt} VE Oda={bt} → FanHızı={ft}",
                    'ateslenme_gucu': derece,
                    'cikti_terimi': ft,
                })
        aktif.sort(key=lambda x: x['ateslenme_gucu'], reverse=True)
        return aktif

    def klasik_kontrol_karsilastir(self, T: float, H: float, S: float) -> float:
        """
        Basit eşik tabanlı (on/off) kontrol sistemi.
        Bulanık sistemle karşılaştırma amacıyla kullanılır.
        """
        T = float(np.clip(T, 0, 40))
        H = float(np.clip(H, 0, 100))
        S = float(np.clip(S, 0, 100))

        # Sıcaklık 0–60
        if T < 15:
            s_skor = 0
        elif T < 25:
            s_skor = 20
        elif T < 32:
            s_skor = 40
        else:
            s_skor = 60

        # Nem 0–25
        if H < 40:
            n_skor = 0
        elif H < 65:
            n_skor = 10
        else:
            n_skor = 25

        # Oda boyutu 0–15
        if S < 30:
            b_skor = 0
        elif S < 60:
            b_skor = 8
        else:
            b_skor = 15

        return float(np.clip(s_skor + n_skor + b_skor, 0, 100))

    def linguistik_yorum(self, fan_hizi: float) -> str:
        """Fan hızı değerine göre insan okunabilir durum döndürür."""
        if fan_hizi < 30:
            return "🟢 Düşük Yük — Konforlu"
        elif fan_hizi < 55:
            return "🟡 Orta Yük — Normal"
        elif fan_hizi < 75:
            return "🟠 Yüksek Yük — Yoğun"
        else:
            return "🔴 Maksimum Yük — Kritik"
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 1. Biyolojik ve Donanımsal Parametreler
AREA_CM2 = 1.14799e-5  # NeuroMorpho'dan alınan yüzey alanı (cm^2)

# Spesifik değerler (1 cm^2 başına düşen standart HH değerleri)
C_m_spec = 1.0  # uF/cm^2 (Spesifik kapasitans)
g_Na_spec = 120.0  # mS/cm^2 (Maksimum sodyum iletkenliği)
g_K_spec = 36.0  # mS/cm^2 (Maksimum potasyum iletkenliği)
g_L_spec = 0.3  # mS/cm^2 (Sızıntı iletkenliği)

# Devredeki gerçek komponent değerleri (Alan ile çarpılmış)
C_m = C_m_spec * AREA_CM2  # Gerçek Kapasitans (uF) -> ~11.5 pF
g_Na = g_Na_spec * AREA_CM2  # Gerçek Na iletkenliği (mS)
g_K = g_K_spec * AREA_CM2  # Gerçek K iletkenliği (mS)
g_L = g_L_spec * AREA_CM2  # Gerçek Sızıntı iletkenliği (mS)

# İyonların tersine dönme potansiyelleri (Batarya değerleri - mV)
E_Na = 50.0
E_K = -77.0
E_L = -54.387


# 2. Kapı (Gating) Değişkenleri için Alfa ve Beta Fonksiyonları
def alpha_m(V): return 0.1 * (V + 40.0) / (1.0 - np.exp(-(V + 40.0) / 10.0))


def beta_m(V):  return 4.0 * np.exp(-(V + 65.0) / 18.0)


def alpha_h(V): return 0.07 * np.exp(-(V + 65.0) / 20.0)


def beta_h(V):  return 1.0 / (1.0 + np.exp(-(V + 35.0) / 10.0))


def alpha_n(V): return 0.01 * (V + 55.0) / (1.0 - np.exp(-(V + 55.0) / 10.0))


def beta_n(V):  return 0.125 * np.exp(-(V + 65) / 80.0)


# 3. Diferansiyel Denklem Sistemi
def hodgkin_huxley(y, t, I_inj):
    V, m, h, n = y

    # İyon kanalı akımları
    I_Na = g_Na * (m ** 3) * h * (V - E_Na)
    I_K = g_K * (n ** 4) * (V - E_K)
    I_L = g_L * (V - E_L)

    # Zamanla değişimler (Türevler)
    dVdt = (I_inj(t) - I_Na - I_K - I_L) / C_m
    dmdt = alpha_m(V) * (1 - m) - beta_m(V) * m
    dhdt = alpha_h(V) * (1 - h) - beta_h(V) * h
    dndt = alpha_n(V) * (1 - n) - beta_n(V) * n

    return [dVdt, dmdt, dhdt, dndt]


# 4. Simülasyon Zamanı ve Dış Akım (Uyarıcı)
t = np.arange(0.0, 50.0, 0.01)  # 0 ile 50 ms arası, 0.01 ms adımlarla


# Dışarıdan verilecek akım (I_ext). Alan çok küçük olduğu için akım da nano/piko amper seviyesinde.
# 10. ms ile 40. ms arasında devreye 0.2 nanoamper (0.0002 uA) akım veriyoruz.
def I_inj(t):
    return 0.0002 if 10 <= t <= 40 else 0.0


# 5. Başlangıç Koşulları
V0 = -65.0  # Dinlenme potansiyeli
m0 = alpha_m(V0) / (alpha_m(V0) + beta_m(V0))
h0 = alpha_h(V0) / (alpha_h(V0) + beta_h(V0))
n0 = alpha_n(V0) / (alpha_n(V0) + beta_n(V0))
y0 = [V0, m0, h0, n0]

# 6. Çözümleyici (Solver)
solution = odeint(hodgkin_huxley, y0, t, args=(I_inj,))
V = solution[:, 0]

# 7. Grafiği Çizdirme
plt.figure(figsize=(10, 5))
plt.plot(t, V, 'b', linewidth=2, label='Zar Voltajı (Aksiyon Potansiyeli)')
plt.title('Hodgkin-Huxley Modeli (Soma Alanı: 1148 $\mu m^2$)')
plt.xlabel('Zaman (ms)')
plt.ylabel('Voltaj (mV)')
plt.grid(True)
plt.axhline(y=-65, color='r', linestyle='--', alpha=0.5, label='Dinlenme Potansiyeli')
plt.legend()
plt.show()
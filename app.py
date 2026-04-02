import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# 網頁基本設定
st.set_page_config(page_title="黑體輻射模擬器", layout="centered")

# --- 物理常數與基準值 ---
h, c, kB = 6.626e-34, 3.0e8, 1.38e-23
sigma = 5.67e-8  # 史蒂芬-波茲曼常數
T_sun = 5773     # 太陽基準溫度 (K)
P_sun = sigma * (T_sun**4) 

st.title("🌡️ 黑體輻射互動模擬器")
st.markdown("---")

# 1. 數值輸入框 (設定為 Kelvin)
temp_k = st.number_input("請輸入絕對溫度 (Kelvin):", min_value=100, max_value=20000, value=5773, step=100)

# 2. 物理計算
total_intensity = sigma * (temp_k**4)
ratio_to_sun = total_intensity / P_sun
peak_wave_nm = (2.898e-3 / temp_k) * 1e9

# 3. 顯示中文數據分析 (這部分不會亂碼)
st.subheader("📊 實驗數據分析")
col1, col2 = st.columns(2)
with col1:
    st.metric("波峰波長 (Peak)", f"{peak_wave_nm:.1f} nm")
    st.write(f"**總輻射強度:** \n {total_intensity:.2e} W/m²")
with col2:
    st.metric("相對於太陽光度比值", f"{ratio_to_sun:.3f} L⨀")
    if 5700 <= temp_k <= 5850:
        st.success("接近太陽溫度")
    elif temp_k < 3050:
        st.warning("接近白熾燈泡溫度")

# 4. 繪圖準備 (Planck's Law)
waves_nm = np.linspace(50, 4000, 1000)
waves_m = waves_nm * 1e-9
with np.errstate(over='ignore', divide='ignore'):
    intensity = (2 * h * c**2) / (waves_m**5 * (np.exp((h * c) / (waves_m * kB * temp_k)) - 1))

# 5. 繪製圖表
fig, ax = plt.subplots(figsize=(10, 6))

# 🌟 核心視覺化升級：加入彩虹漸層背景 🌟
# 定義可見光範圍
vis_min, vis_max = 400, 700 

# 建立彩虹色譜矩陣
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

# 在圖表中鋪上彩虹
# extent 定義了彩虹在 X 軸(波長)與 Y 軸(強度)的範圍
ax.imshow(gradient, aspect='auto', cmap=cm.rainbow, alpha=0.4,
          extent=[vis_min, vis_max, 0, np.max(intensity) * 1.1], zorder=0)

# 繪製黑體輻射曲線 (放在彩虹上面)
ax.plot(waves_nm, intensity, color='black', lw=2.5, zorder=10)

# 標註坡峰虛線
ax.axvline(peak_wave_nm, color='red', linestyle='--', alpha=0.5, zorder=15)

# 圖表格式設定 (使用英文避開亂碼)
ax.set_xlabel("Wavelength (nm)", fontsize=12)
ax.set_ylabel("Spectral Radiance", fontsize=12)
ax.set_title(f"Blackbody Spectrum at {temp_k} K", fontsize=14)
ax.set_xlim(0, 3500)
# 動態設定 Y 軸上限，確保波峰永遠可見
ax.set_ylim(0, np.max(intensity) * 1.1) 
ax.grid(True, linestyle=':', alpha=0.6)

# 顯示圖表
st.pyplot(fig)

# ==============================================================================
# PRISM 2.2 CANONICAL FULL-GRID (87,009 TEMPLATES) 4,096s DISJOINT BACKGROUND
# ==============================================================================
# - Exactly matches the on-source discovery grid of Paper I:
#     * freqs:   np.arange(20.0, 500.1, 5.0)     (97 frequencies)
#     * centers: np.arange(-0.180, 0.041, 0.010) (23 centers)
#     * widths:  [0.015, 0.030, 0.060]            (3 widths)
#     * lags:    np.arange(-0.012, 0.0121, 0.002) (13 lags)
#     * TOTAL TEMPLATES: 97 * 23 * 3 * 13 = 87,009 templates
# - Evaluates continuous 4,096s GWOSC strain data for H1 and L1.
# - Evaluates all 1,018 disjoint (0.0% overlap) 4.0s windows outside merger +-10s.
# ==============================================================================

import os
import time
import argparse
import h5py
import numpy as np
import scipy.signal as signal
import pandas as pd

CONFIGS = {
    'GW190521': {
        'gps_merger': 1242459857.5,
        'gps_file_start': 1242456064,
        'h1_path': r'E:\RIUD_T7_MIRROR_2026-10-26\03_EXTERNAL_VALIDATION\RIUD_LIGO_SXS_SEOBNR_MATCHED_TRIPLETS_R0_20261122\gwosc_strain\GW190521_074359\H-H1_GWOSC_O3a_4KHZ_R1-1242456064-4096.hdf5',
        'l1_path': r'E:\RIUD_T7_MIRROR_2026-10-26\03_EXTERNAL_VALIDATION\RIUD_LIGO_SXS_SEOBNR_MATCHED_TRIPLETS_R0_20261122\gwosc_strain\GW190521_074359\L-L1_GWOSC_O3a_4KHZ_R1-1242456064-4096.hdf5',
        'primary_benchmark': 22.410994,
        'f0_peak': 125.0
    },
    'GW150914': {
        'gps_merger': 1126259462.4,
        'gps_file_start': 1126257415,
        'h1_path': r'E:\riud\long_strain_cache\GW150914\H-H1_GWOSC_4KHZ_R1-1126257415-4096.hdf5',
        'l1_path': r'E:\riud\long_strain_cache\GW150914\L-L1_GWOSC_4KHZ_R1-1126257415-4096.hdf5',
        'primary_benchmark': 16.901189,
        'f0_peak': 190.0
    },
    'GW170104': {
        'gps_merger': 1167559936.6,
        'gps_file_start': 1167557889,
        'h1_path': r'E:\riud\long_strain_cache\GW170104\H-H1_GWOSC_4KHZ_R1-1167557889-4096.hdf5',
        'l1_path': r'E:\riud\long_strain_cache\GW170104\L-L1_GWOSC_4KHZ_R1-1167557889-4096.hdf5',
        'primary_benchmark': 9.805093,
        'f0_peak': 220.0
    },
    'GW170814': {
        'gps_merger': 1186741861.5,
        'gps_file_start': 1186739814,
        'h1_path': r'E:\riud\long_strain_cache\GW170814\H-H1_GWOSC_4KHZ_R1-1186739814-4096.hdf5',
        'l1_path': r'E:\riud\long_strain_cache\GW170814\L-L1_GWOSC_4KHZ_R1-1186739814-4096.hdf5',
        'primary_benchmark': 20.393390,
        'f0_peak': 120.0
    }
}

def build_full_discovery_bank(fs=1024.0, win_len=4096):
    print("Precomputing canonical full-grid 87,009 templates (float32)...")
    t0 = time.time()
    t_grid = np.arange(win_len) / fs - 2.0
    
    centers = np.arange(-0.180, 0.041, 0.010) # 23
    widths = [0.015, 0.030, 0.060]            # 3
    freqs = np.arange(20.0, 500.1, 5.0)       # 97
    lags = np.arange(-0.012, 0.0121, 0.002)   # 13
    
    total = len(centers) * len(widths) * len(freqs) * len(lags)
    assert total == 87009, f"Expected 87009 templates, got {total}"
    
    mat_H = np.zeros((total, win_len), dtype=np.float32)
    mat_L = np.zeros((total, win_len), dtype=np.float32)
    coords = []
    
    idx = 0
    for w in widths:
        for c in centers:
            for f0 in freqs:
                x_h = t_grid - c
                y_h = np.zeros_like(t_grid)
                ih = x_h >= 0
                y_h[ih] = np.exp(-x_h[ih] / w) * np.sin(2.0 * np.pi * f0 * x_h[ih])
                y_h -= np.mean(y_h)
                nh = np.linalg.norm(y_h)
                th = (y_h / nh).astype(np.float32) if nh > 0 else y_h.astype(np.float32)
                
                for lag in lags:
                    x_l = t_grid - (c + lag)
                    y_l = np.zeros_like(t_grid)
                    il = x_l >= 0
                    y_l[il] = np.exp(-x_l[il] / w) * np.sin(2.0 * np.pi * f0 * x_l[il])
                    y_l -= np.mean(y_l)
                    nl = np.linalg.norm(y_l)
                    tl = (y_l / nl).astype(np.float32) if nl > 0 else y_l.astype(np.float32)
                    
                    mat_H[idx] = th
                    mat_L[idx] = tl
                    coords.append((round(float(c), 3), float(w), float(f0), round(float(lag), 4)))
                    idx += 1
                    
    print(f"Bank built in {time.time() - t0:.2f}s. Matrix size: {mat_H.nbytes / 1e6:.1f} MB per detector.")
    return mat_H, mat_L, coords

def whiten_4s_block(x_block, f_psd, psd_vals, fs=1024.0, band=(20.0, 500.0)):
    n = len(x_block)
    rfft_freq = np.fft.rfftfreq(n, d=1.0/fs)
    psd_interp = np.interp(rfft_freq, f_psd, psd_vals)
    mask = (rfft_freq >= band[0]) & (rfft_freq <= band[1]) & (psd_interp > 0)
    w = signal.windows.tukey(n, alpha=0.1)
    xf = np.fft.rfft(x_block * w)
    whiten_fd = np.zeros_like(xf, dtype=complex)
    whiten_fd[mask] = xf[mask] / np.sqrt(psd_interp[mask])
    td = np.fft.irfft(whiten_fd, n=n)
    td = np.nan_to_num(td)
    med = np.median(td)
    std = np.std(td)
    normed = (td - med) / std if std > 0 else td - med
    return normed.astype(np.float32)

def run_event(event_name, mat_H, mat_L, coords):
    cfg = CONFIGS[event_name]
    print("=" * 70)
    print(f"RUNNING EXACT CANONICAL 87,009-GRID BACKGROUND FOR: {event_name}")
    print(f"Benchmark: {cfg['primary_benchmark']} (Peak: {cfg['f0_peak']} Hz)")
    print("=" * 70)
    
    t0 = time.time()
    with h5py.File(cfg['h1_path'], 'r') as fH:
        sH_4k = fH['strain/Strain'][:]
        h_dq = fH['quality/simple/DQmask'][:]
    with h5py.File(cfg['l1_path'], 'r') as fL:
        sL_4k = fL['strain/Strain'][:]
        l_dq = fL['quality/simple/DQmask'][:]
        
    fs = 1024.0
    sH = signal.decimate(sH_4k, 4)
    sL = signal.decimate(sL_4k, 4)
    win_len = int(4.0 * fs)
    
    t_merger_rel = cfg['gps_merger'] - cfg['gps_file_start']
    exclude_start = t_merger_rel - 10.0
    exclude_end = t_merger_rel + 10.0
    
    # Estimate PSD on 512s clean off-source window
    psd_start = int(max(0, t_merger_rel - 520.0))
    psd_end = int(max(0, t_merger_rel - 8.0))
    if psd_end - psd_start < 200:
        psd_start = 100
        psd_end = int(t_merger_rel - 20)
        
    off_h = sH[int(psd_start * fs) : int(psd_end * fs)]
    off_l = sL[int(psd_start * fs) : int(psd_end * fs)]
    
    f_h, psd_h = signal.welch(off_h, fs=fs, nperseg=win_len, noverlap=win_len//2, average='median')
    f_l, psd_l = signal.welch(off_l, fs=fs, nperseg=win_len, noverlap=win_len//2, average='median')
    
    n_windows = 4096 // 4
    results = []
    
    t_eval_start = time.time()
    for i in range(n_windows):
        t_start = i * 4.0
        t_end = t_start + 4.0
        
        if not (t_end <= exclude_start or t_start >= exclude_end):
            continue
            
        sec_idx = range(int(t_start), int(t_end))
        h_flags = h_dq[sec_idx]
        l_flags = l_dq[sec_idx]
        
        cbc_ok = int(np.all((h_flags & 7) == 7) and np.all((l_flags & 7) == 7))
        strict_ok = int(np.all(h_flags == 127) and np.all(l_flags == 127))
        
        idx_start = int(t_start * fs)
        block_h = sH[idx_start : idx_start + win_len]
        block_l = sL[idx_start : idx_start + win_len]
        
        if len(block_h) < win_len or len(block_l) < win_len:
            continue
            
        w_h = whiten_4s_block(block_h, f_h, psd_h, fs=fs)
        w_l = whiten_4s_block(block_l, f_l, psd_l, fs=fs)
        
        zH_all = np.dot(mat_H, w_h)
        zL_all = np.dot(mat_L, w_l)
        
        same_all = np.abs(zH_all + zL_all) * (1.0 / np.sqrt(2.0, dtype=np.float32))
        opp_all = np.abs(zH_all - zL_all) * (1.0 / np.sqrt(2.0, dtype=np.float32))
        coh_all = np.maximum(same_all, opp_all)
        
        best_idx = np.argmax(coh_all)
        best_coh = float(coh_all[best_idx])
        best_zH = float(zH_all[best_idx])
        best_zL = float(zL_all[best_idx])
        best_c, best_w, best_f0, best_lag = coords[best_idx]
        best_mode = 'same' if same_all[best_idx] >= opp_all[best_idx] else 'opposite'
        
        bm = cfg['primary_benchmark']
        results.append({
            'window_index': i,
            't_start_rel_sec': round(t_start, 2),
            't_end_rel_sec': round(t_end, 2),
            'gps_start': round(cfg['gps_file_start'] + t_start, 2),
            'cbc_cat12_pass': cbc_ok,
            'strict_127_pass': strict_ok,
            'max_coherent_score': round(best_coh, 6),
            'zH1': round(best_zH, 6),
            'zL1': round(best_zL, 6),
            'f0_Hz': best_f0,
            'center_sec': best_c,
            'width_sec': best_w,
            'lag_sec': best_lag,
            'mode': best_mode,
            'on_source_benchmark': bm,
            'exceed': int(best_coh >= bm)
        })
        
    eval_elapsed = time.time() - t_eval_start
    df = pd.DataFrame(results)
    print(f"Evaluated {len(df)} windows across 87,009 templates in {eval_elapsed:.2f}s ({eval_elapsed/len(df)*1000:.1f} ms/window).")
    
    # Save outputs to multiple canonical locations
    out_dirs = [
        r'E:\riud\GW190521_calibration',
        r'E:\SEND\PAPER_1_CHECK'
    ]
    
    for d in out_dirs:
        os.makedirs(d, exist_ok=True)
        csv_p = os.path.join(d, f'{event_name}_CANONICAL_87009_GRID_4096S_BACKGROUND.csv')
        xlsx_p = os.path.join(d, f'{event_name}_CANONICAL_87009_GRID_4096S_BACKGROUND.xlsx')
        df.to_csv(csv_p, index=False)
        df.to_excel(xlsx_p, index=False)
        print(f"Saved: {csv_p}")
        
    scores = df['max_coherent_score'].values
    print("-" * 70)
    print(f"EVENT: {event_name}")
    print(f"  Windows Evaluated: {len(df)} (Overlap: 0.0%)")
    print(f"  CBC CAT1+2 Pass:  {df['cbc_cat12_pass'].sum()} / {len(df)}")
    print(f"  Strict DQ Pass:    {df['strict_127_pass'].sum()} / {len(df)}")
    print(f"  Score Min:         {scores.min():.6f}")
    print(f"  Score Median:      {np.median(scores):.6f}")
    print(f"  Score p99:         {np.percentile(scores, 99):.6f}")
    print(f"  Score Max:         {scores.max():.6f}")
    print(f"  On-source Score:   {cfg['primary_benchmark']:.6f}")
    print(f"  Exceedances:       {df['exceed'].sum()} / {len(df)}")
    print("=" * 70)
    return df

if __name__ == '__main__':
    mat_H, mat_L, coords = build_full_discovery_bank()
    
    ap = argparse.ArgumentParser()
    ap.add_argument('--event', default='ALL', choices=['ALL', 'GW190521', 'GW150914', 'GW170104', 'GW170814'])
    args = ap.parse_args()
    
    events_to_run = ['GW190521', 'GW150914', 'GW170104', 'GW170814'] if args.event == 'ALL' else [args.event]
    
    all_summaries = []
    for ev in events_to_run:
        df = run_event(ev, mat_H, mat_L, coords)
        s = df['max_coherent_score'].values
        bm = CONFIGS[ev]['primary_benchmark']
        all_summaries.append({
            'Event': ev,
            'GPS_Merger': CONFIGS[ev]['gps_merger'],
            'Templates_Searched': len(coords),
            'Frequency_Range': '20.0 - 500.0 Hz (97 freqs, step 5 Hz)',
            'Centers_Range': '-0.180 to +0.040 s (23 centers, step 0.010 s)',
            'Widths_Tested': '[0.015, 0.030, 0.060] s (3 widths)',
            'Lags_Tested': '-0.012 to +0.012 s (13 lags, step 0.002 s)',
            'On_Source_Score': bm,
            'Tested_Windows': len(df),
            'Window_Overlap': '0.0%',
            'CBC_Passed_Windows': int(df['cbc_cat12_pass'].sum()),
            'Strict_DQ_Passed_Windows': int(df['strict_127_pass'].sum()),
            'Sample_Min_Score': round(float(np.min(s)), 6),
            'Sample_Median_Score': round(float(np.median(s)), 6),
            'Sample_p99_Score': round(float(np.percentile(s, 99)), 6),
            'Sample_Max_Score': round(float(np.max(s)), 6),
            'Observed_Exceedance_Rate': f"{int(df['exceed'].sum())} / {len(df)}"
        })
        
    master_df = pd.DataFrame(all_summaries)
    for d in [r'E:\riud\GW190521_calibration', r'E:\SEND\PAPER_1_CHECK']:
        m_csv = os.path.join(d, 'PAPER_I_SECTION_4_2_CANONICAL_87009_GRID_MASTER.csv')
        m_xlsx = os.path.join(d, 'PAPER_I_SECTION_4_2_CANONICAL_87009_GRID_MASTER.xlsx')
        master_df.to_csv(m_csv, index=False)
        master_df.to_excel(m_xlsx, index=False)
        print(f"Saved master table: {m_csv}")
    print("\nALL COMPLETED SUCCESSFULLY!")

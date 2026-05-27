import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# --- KONFIGURASI DASHBOARD ---
st.set_page_config(page_title="IDX Stock Screener", layout="wide")
st.title("🔍 IDX Quantitative Stock Screener V3.0")
st.markdown("Mesin Pemindai Sinyal Saham Berdasarkan Algoritma Alpha Project")

# --- DAFTAR SELURUH SAHAM IDX ---
raw_tickers = (
    "AALI,ABBA,ABDA,ABMM,ACES,ACST,ADCP,ADES,ADHI,ADMF,ADMR,ADRO,AGAR,AGII,AGRO,AHA,AIMS,AISA,AKKU,AKPI,"
    "AKRA,AKSI,ALDO,ALKA,ALMI,ALTO,AMAG,AMAN,AMAR,AMFG,AMIN,AMMN,AMOR,AMRT,ANDI,ANJT,ANTM,APEX,APIC,APII,"
    "APLI,APLN,ARCI,ARGO,ARII,ARKA,ARKO,ARMY,ARNA,ARTA,ARTI,ASBI,ASDM,ASGR,ASHA,ASII,ASJT,ASLC,ASMI,ASPI,"
    "ASRI,ASRM,ASSA,ASTA,ATIC,AUTO,AYLS,BABP,BACA,BAJA,BALI,BAMB,BAPA,BAPI,BATA,BAUT,BAYU,BBCA,BBHI,BBKP,"
    "BBLD,BBMD,BBNI,BBRI,BBRM,BBSS,BBTN,BBYB,BCAP,BCIC,BDMN,BEKS,BELL,BESS,BEST,BFIN,BGTG,BHAT,BINA,BIPI,"
    "BIPP,BIRD,BISI,BJBR,BJTM,BKDP,BKSL,BKSW,BLTA,BLTZ,BLUE,BMAS,BMSR,BMTR,BNBA,BNBR,BNGA,BNII,BNLI,BOBA,"
    "BOLA,BOLT,BOSS,BPFI,BPII,BPTR,BRMS,BRNA,BRPT,BSDE,BSIM,BSML,BSSR,BSWD,BTEK,BTEL,BTON,BTPN,BTPS,BUDI,"
    "BUKK,BULL,BUMI,BUVA,BVIC,BWPT,BYAN,CAKK,CAMP,CANI,CAPC,CARS,CASA,CASS,CBEZ,CEKA,CENT,CFIN,CINT,CITA,"
    "CITY,CLEO,CLPI,CMNP,CMPP,CMRY,CNKO,CNTX,COAL,COCO,CPIN,CPRI,CPRO,CRAB,CSAP,CSIS,CSMI,CTBN,CTRA,CTTH,"
    "CUAN,DART,DAYA,DCII,DEAL,DEFI,DEWA,DGIK,DIAN,DMMX,DOID,DPNS,DPUM,DSFI,DSNG,DSSA,DUTI,DVLA,DWGL,DYAN,"
    "EAST,ECII,EDII,EKAD,ELSA,ELTY,EMDE,EMTK,ENAK,ENRG,ENVY,EPMT,ERAA,ERTX,ESIP,ESSA,ESTA,ESTI,ETWA,EXCL,"
    "FAPA,FAST,FASW,FILM,FIMP,FIRE,FISH,FITI,FLMC,FMII,FOOD,FORU,FPNI,FREN,GAMA,GDST,GDYR,GEMA,GEMS,GGRM,"
    "GGRP,GHON,GIAA,GJTL,GLOB,GLVA,GMFI,GMTD,GOLD,GOLL,GOTO,GPRA,GPSO,GRCE,GTBO,GWSA,GZCO,HADE,HAIS,HANA,"
    "HDFA,HDIT,HEAL,HELI,HERO,HEXA,HITS,HKMU,HMSP,HOKI,HOME,HOPE,HRME,HRTA,HRUM,IATA,IBFN,IBST,ICBP,ICON,"
    "IDPR,IGAR,IIKP,IKAN,IKBI,IMAS,IMJS,IMPC,INAF,INAI,INCF,INCO,INDA,INDF,INDO,INDR,INDS,INDX,INET,INFA,"
    "ININ,INKP,INMF,INOC,INOV,INPC,INPP,INPS,INRU,INTA,INTD,INTP,IPAC,IPCC,IPCM,IPPE,IPTV,IRRA,ISAT,ISSP,"
    "ITIC,ITMA,ITMG,JAST,JAWA,JCON,JIHD,JKON,JMAS,JPFA,JRPT,JSPT,JTPE,KAEF,KARR,KBLI,KBLM,KBLV,KBRI,KDSI,"
    "KEEN,KEJU,KIAS,KICI,KIGL,KIJA,KINO,KIOS,KLBF,KMDS,KMED,KOBX,KOIN,KONI,KOPI,KOTA,KPAL,KPAS,KPIG,KRYA,"
    "KSTC,KUAS,LAAI,LABA,LAND,LAPD,LCKM,LCNG,LEAD,LFLO,LINK,LION,LMAS,LMPI,LMSH,LPCK,LPGI,LPIN,LPKR,LPLI,"
    "LPPF,LPPS,LRNA,LSIP,LTLS,LUCK,LUGAR,MABA,MACU,MAGP,MAIN,MAMI,MAPA,MAPB,MAPI,MARI,MARK,MASA,MAXI,MAYA,"
    "MBAP,MBSS,MBTO,MCAS,MCOR,MDIA,MDKA,MDKI,MDLN,MDRN,MEDC,MEGA,MERK,META,MFIN,MFMI,MGNA,MGRO,MICE,MIDI,"
    "MIKA,MINA,MIRA,MITI,MKNT,MKPI,MLBI,MLIA,MLPL,MLPT,MMSI,MNCN,MOLI,MORA,MPMX,MPOX,MPPA,MRAT,MREI,MSIN,"
    "MSKY,MTDL,MTFN,MTLA,MTMH,MTPS,MTRA,MTSM,MUTU,MYOR,MYRX,MYTX,NANO,NAPS,NATA,NAVT,NELY,NETV,NFCX,NICK,"
    "NICL,NISP,NOBU,NPGF,NRCA,NSSS,NTBK,NUSA,NZIA,OASA,OBMD,OCAP,OILS,OKAS,OMRE,OPMS,PADI,PALM,PAMG,PANI,"
    "PANR,PANS,PBID,PBRX,PBSA,PCAR,PDES,PEGE,PEHA,PGAS,PGEO,PGJO,PGLI,PGUN,PICO,PJAA,PKPK,PLAS,PLIN,PMJS,"
    "PNBN,PNBS,PNGO,PNIN,PNLF,PNSE,POLA,POLI,POLL,POLU,POLY,POOL,PORT,POSA,PRAS,PRDA,PRIM,PSAB,PSDN,PSGO,"
    "PSKT,PTBA,PTIS,PTPP,PTPW,PTRO,PTSN,PTSP,PUDP,PURA,PUTA,PZZA,RAFI,RALF,RAMA,RALS,RANC,RBMS,RCCC,RDTX,"
    "REAL,RELI,RICY,RIGS,RIMO,RINA,RLFS,RMBA,ROKI,ROMA,ROTI,SAGE,SAME,SAMF,SAPX,SATU,SCCO,SCMA,SCNP,SCPI,"
    "SDMU,SDPC,SDRA,SEMA,SGER,SGRO,SHID,SIDO,SILO,SIMA,SIMP,SINI,SION,SIPD,SKBM,SKLT,SKRN,SKYB,SMAR,SMBR,"
    "SMCB,SMDR,SMGR,SMIL,SMKL,SMLE,SMMA,SMMT,SMRA,SMRU,SMSM,SNLK,SOCI,SOFA,SOHO,SONA,SOSS,SOTO,SPMA,SPTO,"
    "SQMI,SRAJ,SRIL,SRSN,SRTG,SSIA,SSMS,SSTP,STAA,STAN,STTP,SUGI,SULA,SULI,SUPR,SURE,SWAT,TAXI,TAYS,TBIG,"
    "TBLA,TBMS,TCID,TCPI,TEBE,TECH,TELE,TFAS,TFCO,TGKA,TIFA,TINS,TIRA,TIRT,TKIM,TLKM,TMAS,TMPO,TNCA,TOBA,"
    "TOYS,TPIA,TRIL,TRIM,TRIN,TRIS,TRJA,TRKU,TRST,TRUE,TRUK,TSPC,TUGU,TURI,UANG,UCID,UFOE,ULTJ,UNIC,UNIQ,"
    "UNIT,UNSP,UNTR,UNVR,URBN,VIVA,VOKS,VRNA,WAPO,WATA,WEGE,WICO,WIFI,WIIM,WIKA,WINS,WMMT,WOMF,WOOD,WOWS,"
    "WSBP,WSKT,WTON,YELO,YPAS,YULE,ZATA,ZBRA,ZINC"
)
idx_tickers = sorted(list(set(raw_tickers.split(','))))

# --- ENGINE SCREENER UNTUK SATU SAHAM ---
def scan_single_stock(ticker):
    try:
        # Kita ambil data 250 hari terakhir (~1 tahun) untuk menghitung MA 200 dengan aman
        stock = yf.Ticker(f"{ticker}.JK")
        df = stock.history(period="1y")
        
        if df.empty or len(df) < 20: # Skip jika data tidak lengkap
            return None
        
        df.index = df.index.tz_localize(None)

        # Hitung Indikator Dasar
        df['SMA_5'] = df['Close'].rolling(window=5).mean()
        df['Value_Trx'] = df['Close'] * df['Volume']
        df['Resisten_20'] = df['High'].rolling(window=20).max()
        df['Support_20'] = df['Low'].rolling(window=20).min()
        df['MA_50'] = df['Close'].rolling(window=50).mean()
        df['MA_200'] = df['Close'].rolling(window=200).mean()
        
        # Bollinger Bands
        df['BB_MID'] = df['Close'].rolling(window=20).mean()
        df['STD_20'] = df['Close'].rolling(window=20).std()
        df['BB_LOWER'] = df['BB_MID'] - (2 * df['STD_20'])

        # Ambil baris TERAKHIR (Hari ini / Hari Bursa Terakhir)
        # Serta baris-baris sebelumnya untuk logika H-1, H-2, dst.
        h0 = df.iloc[-1]
        h1 = df.iloc[-2]
        h2 = df.iloc[-3]
        h3 = df.iloc[-4]

        triggered_strategies = []

        # 1. Sinyal V1.1
        if (h1['Close'] < h1['Open']) and (h1['Close'] < h1['SMA_5']) and (h0['Close'] > h0['Open']) and (h0['Close'] > h0['SMA_5']):
            triggered_strategies.append("V1.1 (SMA 5 Breakout Reversal)")

        # 2. Sinyal V1.2
        if (h1['Close'] > h1['Open']) and (h1['Close'] > h1['SMA_5']) and (h0['Close'] < h0['Open']) and (h0['Close'] >= h0['SMA_5']) and (((h0['Close'] - h0['SMA_5']) / h0['SMA_5']) <= 0.02):
            triggered_strategies.append("V1.2 (Pullback SMA 5)")

        # 3. Sinyal V1.3
        if (h1['Close'] > h1['Open']) and (h1['Close'] > h1['SMA_5']) and (h2['Close'] > h2['Open']) and (h2['Close'] > h2['SMA_5']) and (h3['Close'] > h3['Open']) and (h3['Close'] > h3['SMA_5']) and (h0['Close'] > h1['Resisten_20']):
            triggered_strategies.append("V1.3 (Breakout Resisten)")

        # 4. Sinyal V2.1
        if (h1['Close'] < h1['SMA_5']) and (h0['Close'] > h0['SMA_5']) and (((h0['Close'] - h0['SMA_5']) / h0['SMA_5']) * 100 >= 10) and (h0['Value_Trx'] >= 5_000_000_000):
            triggered_strategies.append("V2.1 (Break SMA5 > 10% + Value > 5B)")

        # 5. Sinyal V2.2
        cond_sideways = ((h1['Resisten_20'] - h1['Support_20']) / h1['Support_20']) <= 0.10
        if cond_sideways and (h1['Close'] < h1['SMA_5']) and (h0['Close'] > h0['SMA_5']) and (((h0['Close'] - h0['SMA_5']) / h0['SMA_5']) * 100 >= 10) and (h0['Value_Trx'] >= 5_000_000_000):
            triggered_strategies.append("V2.2 (Sideways Breakout + Value > 5B)")

    # 6. BB Reversal (CUSTOM UPDATE)
        # c1 & c2 = Syarat H-1
        c1 = h1['Low'] < h1['BB_LOWER']
        c2 = h1['Close'] < h1['BB_LOWER']
        
        # c3 sampai c7 = Syarat H-0 (Hari ini)
        c3 = h0['Close'] > h0['BB_LOWER']
        c4 = h0['Value_Trx'] > 1_000_000_000
        c5 = h0['Volume'] > h1['Volume']
        c6 = h0['High'] > h1['High']
        c7 = h0['Close'] > h1['Close']
        
        if c1 and c2 and c3 and c4 and c5 and c6 and c7:
            triggered_strategies.append("BB Reversal (Volume Breakout)")

        # 7. BB Mid Pullback
        if (h1['Close'] > h1['Open']) and (h1['Low'] > h1['BB_MID']) and (h0['Close'] < h0['Open']) and (h0['Close'] >= h0['BB_MID']) and (h0['Low'] <= h0['BB_MID'] * 1.02):
            triggered_strategies.append("BB MID (Pullback to Mid Band)")

        # 8. MA50 Pullback
        if (h0['MA_50'] > h0['MA_200']) and (h1['Close'] > h1['Open']) and (h1['Low'] > h1['MA_50']) and (h0['Close'] < h0['Open']) and (h0['Close'] >= h0['MA_50']) and (h0['Low'] <= h0['MA_50'] * 1.02):
            triggered_strategies.append("MA 50 / 200 (Uptrend Pullback)")

        # Jika ada rumus yang terpicu, kembalikan datanya
        if triggered_strategies:
            return {
                "Ticker": ticker,
                "Price": round(h0['Close'], 0),
                "Value (Billion)": round(h0['Value_Trx'] / 1e9, 2),
                "Strategies": triggered_strategies
            }
    except Exception as e:
        pass
    return None

# --- UI DAN LOGIKA UTAMA ---
st.sidebar.header("⚙️ Kontrol Pemindai")
max_workers = st.sidebar.slider("Kecepatan Scan (Threads)", 5, 30, 15, help="Semakin tinggi semakin cepat, tapi rentan diblokir Yahoo Finance jika terlalu tinggi.")

# Tombol Utama
if st.button("🚀 MULAI PEMINDAIAN SELURUH SAHAM IDX (REAL-TIME)"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    total_saham = len(idx_tickers)
    
    status_text.markdown(f"**Memulai pemindaian paralel untuk {total_saham} saham...**")
    
    # Menggunakan ThreadPoolExecutor untuk Multithreading agar super cepat
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_single_stock, ticker): ticker for ticker in idx_tickers}
        
        for i, future in enumerate(futures):
            res = future.result()
            if res:
                results.append(res)
            
            # Update Progress Bar
            progress = (i + 1) / total_saham
            progress_bar.progress(progress)
            if i % 20 == 0:
                status_text.markdown(f"🔄 Dipindai: {i+1}/{total_saham} Saham | Ditemukan: {len(results)} potensi")
                
    status_text.success(f"🎉 Pemindaian Selesai! Menemukan {len(results)} saham potensial hari ini.")
    
    if results:
        # Ubah list hasil menjadi DataFrame rapi
        df_all = pd.DataFrame(results)
        
        # Membuat list seluruh strategi unik untuk mapping Tab UI
        all_strategies = [
            "V1.1 (SMA 5 Breakout Reversal)",
            "V1.2 (Pullback SMA 5)",
            "V1.3 (Breakout Resisten)",
            "V2.1 (Break SMA5 > 10% + Value > 5B)",
            "V2.2 (Sideways Breakout + Value > 5B)",
            "BB Reversal (Buy on Lower BB)",
            "BB MID (Pullback to Mid Band)",
            "MA 50 / 200 (Uptrend Pullback)"
        ]
        
        st.markdown("### 📊 Hasil Berdasarkan Strategi")
        
        # Buat Tabs dinamis di Streamlit agar UI/UX bersih dan rapi
        tabs = st.tabs(all_strategies)
        
        for idx, strat in enumerate(all_strategies):
            with tabs[idx]:
                # Filter saham yang mengandung strategi spesifik ini
                filtered_df = df_all[df_all['Strategies'].apply(lambda x: strat in x)].copy()
                
                if filtered_df.empty:
                    st.info(f"Tidak ada saham yang memicu rumus **{strat}** pada hari ini.")
                else:
                    # Rapikan tampilan tabel
                    display_df = filtered_df[["Ticker", "Price", "Value (Billion)"]]
                    st.subheader(f"📈 {len(display_df)} Saham terdeteksi masuk radar:")
                    st.dataframe(display_df, use_container_width=True)
                    
                    # Tambah Tombol Download CSV per Strategi
                    csv = display_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label=f"📥 Download Daftar {strat}",
                        data=csv,
                        file_name=f"screener_{strat.split(' ')[0]}.csv",
                        mime='text/csv',
                    )
    else:
        st.warning("Hari ini tidak ada satu pun saham di IDX yang lolos semua kriteria rumus teknikal di atas.")

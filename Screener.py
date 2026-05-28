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
    "AADI,AALI,ABBA,ABDA,ABMM,ACES,ACRO,ACST,ADCP,ADES,ADHI,ADMF,ADMG,ADMR,ADRO,AEGS,AGAR,AGII,AGRO,AGRS,"
"AHAP,AIMS,AISA,AKKU,AKPI,AKRA,AKSI,ALDO,ALII,ALKA,ALMI,ALTO,AMAG,AMAN,AMAR,AMFG,AMIN,AMMN,AMMS,AMOR,"
"AMRT,ANDI,ANJT,ANTM,APEX,APIC,APII,APLI,APLN,ARCI,AREA,ARGO,ARII,ARKA,ARKO,ARMY,ARNA,ARTA,ARTI,ARTO,"
"ASBI,ASDM,ASGR,ASHA,ASII,ASJT,ASLC,ASLI,ASMI,ASPI,ASPR,ASRI,ASRM,ASSA,ATAP,ATIC,ATLA,AUTO,AVIA,AWAN,"
"AXIO,AYAM,AYLS,BABP,BABY,BACA,BAIK,BAJA,BALI,BANK,BAPA,BAPI,BATA,BATR,BAUT,BAYU,BBCA,BBHI,BBKP,BBLD,"
"BBMD,BBNI,BBRI,BBRM,BBSI,BBSS,BBTN,BBYB,BCAP,BCIC,BCIP,BDKR,BDMN,BEBS,BEEF,BEER,BEKS,BELI,BELL,BESS,"
"BEST,BFIN,BGTG,BHAT,BHIT,BIKA,BIKE,BIMA,BINA,BINO,BIPI,BIPP,BIRD,BISI,BJBR,BJTM,BKDP,BKSL,BKSW,BLES,"
"BLOG,BLTA,BLTZ,BLUE,BMAS,BMBL,BMHS,BMRI,BMSR,BMTR,BNBA,BNBR,BNGA,BNII,BNLI,BOAT,BOBA,BOGA,BOLA,BOLT,"
"BOSS,BPFI,BPII,BPTR,BRAM,BREN,BRIS,BRMS,BRNA,BRPT,BRRC,BSBK,BSDE,BSIM,BSML,BSSR,BSWD,BTEK,BTEL,BTON,"
"BTPN,BTPS,BUAH,BUDI,BUKA,BUKK,BULL,BUMI,BUVA,BVIC,BWPT,BYAN,CAKK,CAMP,CANI,CARE,CARS,CASA,CASH,CASS,"
"CBDK,CBMF,CBPE,CBRE,CBUT,CCSI,CDIA,CEKA,CENT,CFIN,CGAS,CHEK,CHEM,CHIP,CINT,CITA,CITY,CLAY,CLEO,CLPI,"
"CMNP,CMNT,CMPP,CMRY,CNKO,CNMA,CNTB,CNTX,COAL,COCO,COIN,COWL,CPIN,CPRI,CPRO,CRAB,CRSN,CSAP,CSIS,CSMI,"
"CSRA,CTBN,CTRA,CTTH,CUAN,CYBR,DAAZ,DADA,DART,DATA,DAYA,DCII,DEAL,DEFI,DEPO,DEWA,DEWI,DFAM,DGIK,DGNS,"
"DGWG,DIGI,DILD,DIVA,DKFT,DKHH,DLTA,DMAS,DMMX,DMND,DNAR,DNET,DOID,DOOH,DOSS,DPNS,DPUM,DRMA,DSFI,DSNG,"
"DSSA,DUCK,DUTI,DVLA,DWGL,DYAN,EAST,ECII,EDGE,EKAD,ELIT,ELPI,ELSA,ELTY,EMAS,EMDE,EMTK,ENAK,ENRG,ENVY,"
"ENZO,EPAC,EPMT,ERAA,ERAL,ERTX,ESIP,ESSA,ESTA,ESTI,ETWA,EURO,EXCL,FAPA,FAST,FASW,FILM,FIMP,FIRE,FISH,"
"FITT,FLMC,FMII,FOLK,FOOD,FORE,FORU,FPNI,FUJI,FUTR,FWCT,GAMA,GDST,GDYR,GEMA,GEMS,GGRM,GGRP,GHON,GIAA,"
"GJTL,GLOB,GLVA,GMFI,GMTD,GOLD,GOLF,GOLL,GOOD,GOTO,GOTOM,GPRA,GPSO,GRIA,GRPH,GRPM,GSMF,GTBO,GTRA,GTSI,"
"GULA,GUNA,GWSA,GZCO,HADE,HAIS,HAJJ,HALO,HATM,HBAT,HDFA,HDIT,HEAL,HELI,HERO,HEXA,HGII,HILL,HITS,HKMU,"
"HMSP,HOKI,HOME,HOMI,HOPE,HOTL,HRME,HRTA,HRUM,HUMI,HYGN,IATA,IBFN,IBOS,IBST,ICBP,ICON,IDEA,IDPR,IFII,"
"IFSH,IGAR,IIKP,IKAI,IKAN,IKBI,IKPM,IMAS,IMJS,IMPC,INAF,INAI,INCF,INCI,INCO,INDF,INDO,INDR,INDS,INDX,"
"INDY,INET,INKP,INOV,INPC,INPP,INPS,INRU,INTA,INTD,INTP,IOTF,IPAC,IPCC,IPCM,IPOL,IPPE,IPTV,IRRA,IRSX,"
"ISAP,ISAT,ISEA,ISSP,ITIC,ITMA,ITMG,JARR,JAST,JATI,JAWA,JAYA,JECC,JGLE,JIHD,JKON,JMAS,JPFA,JRPT,JSKY,"
"JSMR,JSPT,JTPE,KAEF,KAQI,KARW,KAYU,KBAG,KBLI,KBLM,KBLV,KBRI,KDSI,KDTN,KEEN,KEJU,KETR,KIAS,KICI,KIJA,"
"KING,KINO,KIOS,KJEN,KKES,KKGI,KLAS,KLBF,KLIN,KMDS,KMTR,KOBX,KOCI,KOIN,KOKA,KONI,KOPI,KOTA,KPIG,KRAS,"
"KREN,KRYA,KSIX,KUAS,LABA,LABS,LAJU,LAND,LAPD,LCGP,LCKM,LEAD,LFLO,LIFE,LINK,LION,LIVE,LMAS,LMAX,LMPI,"
"LMSH,LOPI,LPCK,LPGI,LPIN,LPKR,LPLI,LPPF,LPPS,LRNA,LSIP,LTLS,LUCK,LUCY,MABA,MAGP,MAHA,MAIN,MANG,MAPA,"
"MAPB,MAPI,MARI,MARK,MASB,MAXI,MAYA,MBAP,MBMA,MBSS,MBTO,MCAS,MCOL,MCOR,MDIA,MDIY,MDKA,MDKI,MDLA,MDLN,"
"MDRN,MEDC,MEDS,MEGA,MEJA,MENN,MERI,MERK,META,MFMI,MGLV,MGNA,MGRO,MHKI,MICE,MIDI,MIKA,MINA,MINE,MIRA,"
"MITI,MKAP,MKNT,MKPI,MKTR,MLBI,MLIA,MLPL,MLPT,MMIX,MMLP,MNCN,MOLI,MORA,MPIX,MPMX,MPOW,MPPA,MPRO,MPXL,"
"MRAT,MREI,MSIE,MSIN,MSJA,MSKY,MSTI,MTDL,MTEL,MTFN,MTLA,MTMH,MTPS,MTRA,MTSM,MTWI,MUTU,MYOH,MYOR,MYTX,"
"NAIK,NANO,NASA,NASI,NATO,NAYZ,NCKL,NELY,NEST,NETV,NFCX,NICE,NICK,NICL,NIKL,NINE,NIRO,NISP,NOBU,NPGF,"
"NRCA,NSSS,NTBK,NUSA,NZIA,OASA,OBAT,OBMD,OCAP,OILS,OKAS,OLIV,OMED,OMRE,OPMS,PACK,PADA,PADI,PALM,PAMG,"
"PANI,PANR,PANS,PART,PBID,PBRX,PBSA,PCAR,PDES,PDPP,PEGE,PEHA,PEVE,PGAS,PGEO,PGJO,PGLI,PGUN,PICO,PIPA,"
"PJAA,PJHB,PKPK,PLAN,PLAS,PLIN,PMJS,PMMP,PMUI,PNBN,PNBS,PNGO,PNIN,PNLF,PNSE,POLA,POLI,POLL,POLU,POLY,"
"POOL,PORT,POSA,POWR,PPGL,PPRE,PPRI,PPRO,PRAY,PRDA,PRIM,PSAB,PSAT,PSDN,PSGO,PSKT,PSSI,PTBA,PTDU,PTIS,"
"PTMP,PTMR,PTPP,PTPS,PTPW,PTRO,PTSN,PTSP,PUDP,PURA,PURE,PURI,PWON,PYFA,PZZA,RAAM,RAFI,RAJA,RALS,RANC,"
"RATU,RBMS,RCCC,RDTX,REAL,RELF,RELI,RGAS,RICY,RIGS,RIMO,RISE,RLCO,RMKE,RMKO,ROCK,RODA,RONY,ROTI,RSCH,"
"RSGK,RUIS,RUNS,SAFE,SAGE,SAME,SAMF,SAPX,SATU,SBAT,SBMA,SCCO,SCMA,SCNP,SCPI,SDMU,SDPC,SDRA,SEMA,SFAN,"
"SGER,SGRO,SHID,SHIP,SICO,SIDO,SILO,SIMA,SIMP,SINI,SIPD,SKBM,SKLT,SKRN,SKYB,SLIS,SMAR,SMBR,SMCB,SMDM,"
"SMDR,SMGA,SMGR,SMIL,SMKL,SMKM,SMLE,SMMA,SMMT,SMRA,SMRU,SMSM,SNLK,SOCI,SOFA,SOHO,SOLA,SONA,SOSS,SOTS,"
"SOUL,SPMA,SPRE,SPTO,SQMI,SRAJ,SRIL,SRSN,SRTG,SSIA,SSMS,SSTM,STAA,STAR,STRK,STTP,SUGI,SULI,SUNI,SUPA,"
"SUPR,SURE,SURI,SWAT,SWID,TALF,TAMA,TAMU,TAPG,TARA,TAXI,TAYS,TBIG,TBLA,TBMS,TCID,TCPI,TDPM,TEBE,TECH,"
"TELE,TFAS,TFCO,TGKA,TGRA,TGUK,TIFA,TINS,TIRA,TIRT,TKIM,TLDN,TLKM,TMAS,TMPO,TNCA,TOBA,TOOL,TOPS,TOSK,"
"TOTL,TOTO,TOWR,TOYS,TPIA,TPMA,TRAM,TRGU,TRIL,TRIM,TRIN,TRIO,TRIS,TRJA,TRON,TRST,TRUE,TRUK,TRUS,TSPC,"
"TUGU,TYRE,UANG,UCID,UDNG,UFOE,ULTJ,UNIC,UNIQ,UNIT,UNSP,UNTD,UNTR,UNVR,URBN,UVCR,VAST,VERN,VICI,VICO,"
"VINS,VISI,VIVA,VKTR,VOKS,VRNA,VTNY,WAPO,WBSA,WEGE,WEHA,WGSH,WICO,WIDI,WIFI,WIIM,WIKA,WINE,WINR,WINS,"
"WIRG,WMPP,WMUU,WOMF,WOOD,WOWS,WSBP,WSKT,WTON,YELO,YOII,YPAS,YULE,YUPI,ZATA,ZBRA,ZINC,ZONE,ZYRX,"
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

        # ==========================================
        # 1. Rumus V1.1 (Reversal)
        # ==========================================
        c_11_1 = h0['Volume'] > h1['Volume']
        c_11_2 = h1['Close'] < h0['Close']
        c_11_3 = h0['Close'] > h0['SMA_5']
        c_11_4 = h0['Value_Trx'] > 5_000_000_000
        if c_11_1 and c_11_2 and c_11_3 and c_11_4 and c_11_5:
            triggered_strategies.append("V1.1 (Reversal)")

        # ==========================================
        # 2. Rumus V1.2 (Pullback)
        # ==========================================
        c_12_1 = (h0['Close'] > h0['SMA_5']) and (h1['Close'] > h1['SMA_5']) and (h2['Close'] > h2['SMA_5'])
        c_12_2 = (h2['High'] / h3['Close']) >= 1.1
        c_12_3 = h1['Close'] < h2['Close']
        c_12_4 = h0['Close'] < h1['Close']
        c_12_5 = h0['Value_Trx'] > 1_000_000_000
        if c_12_1 and c_12_2 and c_12_3 and c_12_4 and c_12_5 and c_12_6:
            triggered_strategies.append("V1.2 (Pullback)")

        # ==========================================
        # 3. Rumus V1.3 (Continuation/Breakout Resistance)
        # ==========================================
        c_13_1 = h0['Volume'] > h1['Volume']
        c_13_2 = h1['Close'] < h0['Close']
        c_13_3 = (h0['Close'] > h0['SMA_5']) and (h1['Close'] > h1['SMA_5']) and (h2['Close'] > h2['SMA_5'])
        c_13_4 = h0['Value_Trx'] > 5_000_000_000
        c_13_5 = h0['Close'] > h1['Resisten_20']
        c_13_6 = h0['MA_50'] > h0['MA_200']
        if c_13_1 and c_13_2 and c_13_3 and c_13_4 and c_13_5 and c_13_6:
            triggered_strategies.append("V1.3 (Continuation)")

        # 4. Sinyal V2.1
        if (h1['Close'] < h1['SMA_5']) and (h0['Close'] > h0['SMA_5']) and (((h0['Close'] - h0['SMA_5']) / h0['SMA_5']) * 100 >= 10) and (h0['Value_Trx'] >= 5_000_000_000):
            triggered_strategies.append("V2.1 (Break SMA5 > 10% + Value > 5B)")

        # 5. Sinyal V2.2
        cond_sideways = ((h1['Resisten_20'] - h1['Support_20']) / h1['Support_20']) <= 0.10
        if cond_sideways and (h1['Close'] < h1['SMA_5']) and (h0['Close'] > h0['SMA_5']) and (((h0['Close'] - h0['SMA_5']) / h0['SMA_5']) * 100 >= 10) and (h0['Value_Trx'] >= 5_000_000_000):
            triggered_strategies.append("V2.2 (Sideways Breakout + Value > 5B)")

        # Bollinger Bands & EMA (Tambahan)
        df['BB_UPPER'] = df['BB_MID'] + (2 * df['STD_20'])
        df['BB_BANDWIDTH'] = (df['BB_UPPER'] - df['BB_LOWER']) / df['BB_MID']
        df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        
        # Ambil baris TERAKHIR (h0, h1, h2, dll)
        # (pastikan kode di atas ditaruh sebelum deklarasi h0, h1, h2...)

        # ==========================================
        # 6. Rumus BB MID (First Touch Pullback)
        # ==========================================
        c_mid_1 = (h0['Close'] > h0['BB_MID']) and (h0['Close'] <= h0['BB_MID'] * 1.02)
        c_mid_2 = h0['Value_Trx'] > 1_000_000_000
        # Naik tinggi sebelumnya dipastikan dengan EMA Uptrend & Bandwidth melebar
        c_mid_3 = (h0['EMA_10'] > h0['EMA_20']) and (h0['EMA_20'] > h0['EMA_50'])
        c_mid_4 = h0['BB_BANDWIDTH'] >= 0.10
        # Sentuhan pertama (H-1 dan H-2 harga Low masih di atas BB_MID)
        c_mid_6 = (h1['Low'] > h1['BB_MID']) and (h2['Low'] > h2['BB_MID'])
        
        if c_mid_1 and c_mid_2 and c_mid_3 and c_mid_4 and c_mid_5 and c_mid_6:
            triggered_strategies.append("BB MID (First Touch Pullback)")

        # ==========================================
        # 7. Rumus BB Reversal (Volume Breakout)
        # ==========================================
        c_rev_1 = h1['Low'] < h1['BB_LOWER']
        c_rev_2 = h1['Close'] < h1['BB_LOWER'] # Candle kemarin ditutup di bawah BB
        c_rev_3 = h0['Close'] > h0['BB_LOWER'] # Break kembali ke atas BB
        c_rev_4 = h0['Value_Trx'] > 1_000_000_000
        c_rev_5 = h0['Volume'] > h1['Volume'] # Volume naik
        
        if c_rev_1 and c_rev_2 and c_rev_3 and c_rev_4 and c_rev_5 and c_rev_6 and c_rev_7:
            triggered_strategies.append("BB Reversal (Volume Breakout)")

        # Hitung Prev LLV(Low, 5) 
        prev_llv_low_5 = df['Low'].iloc[-6:-1].min()

        # ==========================================
        # 8. MA 50 Pullback (OPTIMIZED + TREND FILTER)
        # ==========================================
        # c1: 5 hari sebelumnya selalu di atas MA 50 (belum pernah nyentuh)
        c_ma50_1 = prev_llv_low_5 > h0['MA_50']
        
        # c2: Garis MA 50 wajib menanjak
        c_ma50_2 = h0['MA_50'] > h1['MA_50']
        
        # c3: Low nyentuh/mendekati MA (maksimal 2%), TAPI Close wajib mantul di atas MA
        c_ma50_3 = (h0['Low'] <= h0['MA_50'] * 1.02) and (h0['Close'] >= h0['MA_50'])
        
        # c4: Likuiditas transaksi hari ini > 1 Miliar
        c_ma50_4 = h0['Value_Trx'] > 1_000_000_000

        # c5: Filter Tren Utama (MA 50 harus berada di atas MA 200)
        c_ma50_5 = h0['MA_50'] > h0['MA_200']
        
        if c_ma50_1 and c_ma50_2 and c_ma50_3 and c_ma50_4 and c_ma50_5:
            triggered_strategies.append("MA 50 (Optimized Pullback)")


        # ==========================================
        # 9. MA 200 Pullback (OPTIMIZED + TREND FILTER)
        # ==========================================
        c_ma200_1 = prev_llv_low_5 > h0['MA_200']
        c_ma200_2 = h0['MA_200'] > h1['MA_200'] 
        c_ma200_3 = (h0['Low'] <= h0['MA_200'] * 1.02) and (h0['Close'] >= h0['MA_200'])
        c_ma200_4 = h0['Value_Trx'] > 1_000_000_000
        
        # Filter Tren Utama (MA 50 harus berada di atas MA 200)
        c_ma200_5 = h0['MA_50'] > h0['MA_200'] 
        
        if c_ma200_1 and c_ma200_2 and c_ma200_3 and c_ma200_4 and c_ma200_5:
            triggered_strategies.append("MA 200 (Optimized Pullback)")

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
            "BB MID (First Touch Pullback)",
            "BB Reversal (Volume Breakout)",
            "MA 50 (Pullback Tolerance)",
            "MA 200 (Pullback Tolerance)"
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

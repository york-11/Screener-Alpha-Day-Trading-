import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- KONFIGURASI DASHBOARD ---
st.set_page_config(page_title="IDX Stock Screener", layout="wide")
st.title("🔍 IDX Quantitative Stock Screener V4.0")
st.markdown("Mesin Pemindai Sinyal Saham — Sinkron dengan Parameter Day Trading Yang Mulia")

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
    "WIRG,WMPP,WMUU,WOMF,WOOD,WOWS,WSBP,WSKT,WTON,YELO,YOII,YPAS,YULE,YUPI,ZATA,ZEUS,ZBRA,ZINC,ZONE,ZYRX,"
)
idx_tickers = sorted(list(set(t for t in raw_tickers.split(',') if t.strip())))


# ============================================================
# ENGINE: SCAN SATU SAHAM 
# ============================================================
def scan_single_stock(ticker: str) -> dict | None:
    try:
        df = yf.Ticker(f"{ticker}.JK").history(period="1y")

        if df.empty or len(df) < 210:
            return None

        df.index = df.index.tz_localize(None)

        # Perhitungan Indikator Kunci
        df['MA_5']        = df['Close'].rolling(5).mean()
        df['MA_50']       = df['Close'].rolling(50).mean()
        df['MA_200']      = df['Close'].rolling(200).mean()
        df['Value_Trx']   = df['Close'] * df['Volume']
        df['Resisten_20'] = df['High'].rolling(20).max()
        df['Support_20']  = df['Low'].rolling(20).min()

        # Bollinger Bands (20, 2)
        df['BB_MID']   = df['Close'].rolling(20).mean()
        df['BB_STD']   = df['Close'].rolling(20).std()
        df['BB_UPPER'] = df['BB_MID'] + 2 * df['BB_STD']
        df['BB_LOWER'] = df['BB_MID'] - 2 * df['BB_STD']
        df['BB_BW']    = (df['BB_UPPER'] - df['BB_LOWER']) / df['BB_MID']

        # EMA Filter
        df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()

        # LLV Kunci
        df['LLV_5'] = df['Low'].shift(1).rolling(5).min()

        h0 = df.iloc[-1]   # Hari ini
        h1 = df.iloc[-2]   # Kemarin
        h2 = df.iloc[-3]   # 2 Hari lalu
        h3 = df.iloc[-4]   # 3 Hari lalu

        triggered = []

        # ==========================================
        # MA 50 (Pullback)
        # ==========================================
        c_ma50 = (
            (h0['LLV_5'] > h0['MA_50'])
            and (h0['Close'] >= h0['MA_50'] * 0.99)
            and (h0['Close'] <= h0['MA_50'] * 1.02)
            and (h0['Value_Trx'] >= 1_000_000_000)
            and (h0['MA_50'] > h0['MA_200'])
            and (h0['Close'] < h0['Open'])
            and (h0['Close'] > h0['MA_50'])
        )
        if c_ma50:
            triggered.append("MA 50 (Pullback)")

        # ==========================================
        # MA 200 (Pullback)
        # ==========================================
        c_ma200 = (
            (h0['LLV_5'] > h0['MA_200'])
            and (h0['Close'] >= h0['MA_200'] * 0.99)
            and (h0['Close'] <= h0['MA_200'] * 1.02)
            and (h0['Value_Trx'] >= 1_000_000_000)
            and (h0['MA_50'] > h0['MA_200'])
            and (h0['Close'] < h0['Open'])
            and (h0['Close'] > h0['MA_200'])
        )
        if c_ma200:
            triggered.append("MA 200 (Pullback)")

        # ==========================================
        # BB MID
        # ==========================================
        c_bb_mid = (
            (h0['Close'] >= h0['BB_MID'] * 0.98)
            and (h0['Close'] <= h0['BB_MID'] * 1.02)
            and (h0['Value_Trx'] >= 1_000_000_000)
            and (h0['EMA_10'] > h0['EMA_20'])
            and (h0['EMA_20'] > h0['EMA_50'])
            and (h0['BB_BW'] >= 0.1)
            and (h0['Close'] > h0['BB_MID'])
            and (h0['Close'] < h0['Open'])
        )
        if c_bb_mid:
            triggered.append("BB MID")

        # ==========================================
        # BB REVERSAL
        # ==========================================
        c_bb_rev = (
            (h1['Low'] < h1['BB_LOWER'])
            and (h1['Close'] < h1['BB_LOWER'])
            and (h0['Close'] > h0['BB_LOWER'])
            and (h0['Value_Trx'] >= 1_000_000_000)
            and (h0['Volume'] > h1['Volume'])
            and (h1['High'] < h0['High'])
            and (h0['Close'] > h1['Close'])
            and (h1['Close'] < h1['Open'])
            and (h0['Close'] > h0['Open'])
        )
        if c_bb_rev:
            triggered.append("BB Reversal")

        # ==========================================
        # SCREENER V1.1 (Reversal)
        # ==========================================
        c_v11 = (
            (h0['Volume'] > h1['Volume'])
            and (h1['Close'] < h0['Close'])
            and (h0['Close'] > h0['MA_5'])
            and (h0['Value_Trx'] >= 5_000_000_000)
            and (h1['Close'] < h1['MA_5'])
            and (h0['Close'] > h0['Open'])
        )
        if c_v11:
            triggered.append("V1.1 (Reversal)")

        # ==========================================
        # SCREENER V1.2 (Pullback)
        # ==========================================
        c_v12 = (
            (h0['Close'] > h0['MA_5'])
            and (h1['Close'] > h1['MA_5'])
            and (h2['Close'] > h2['MA_5'])
            and (h2['High'] / h3['Close'] >= 1.1)
            and (h1['Close'] < h2['Close'])
            and (h0['Close'] < h1['Close'])
            and (h0['Value_Trx'] >= 1_000_000_000)
            and (h0['Close'] < h0['Open'])
        )
        if c_v12:
            triggered.append("V1.2 (Pullback)")

        # ==========================================
        # SCREENER V1.3 (Continuation)
        # ==========================================
        c_v13 = (
            (h0['Volume'] > h1['Volume'])
            and (h1['Close'] < h0['Close'])
            and (h0['Close'] > h0['MA_5'])
            and (h0['Value_Trx'] >= 5_000_000_000)
            and (h1['Close'] > h1['Open']) and (h1['Close'] > h1['MA_5'])
            and (h2['Close'] > h2['Open']) and (h2['Close'] > h2['MA_5'])
            and (h3['Close'] > h3['Open']) and (h3['Close'] > h3['MA_5'])
            and (h0['Close'] > h1['Resisten_20'])
        )
        if c_v13:
            triggered.append("V1.3 (Continuation)")

        # ==========================================
        # SCREENER V2.1 (Reversal Break SMA5 ≥ 10%)
        # ==========================================
        c_v21 = (
            (h0['Volume'] > h1['Volume'])
            and (h1['Close'] < h0['Close'])
            and (h0['Close'] > h0['MA_5'])
            and (h0['Value_Trx'] >= 5_000_000_000)
            and (h0['High'] / h1['Close'] >= 1.10)
            and (h1['Close'] < h1['MA_5'])
        )
        if c_v21:
            triggered.append("V2.1 (Reversal)")

        # ==========================================
        # SCREENER V2.2 (Sideways Breakout ≥ 10%)
        # ==========================================
        sideways_range = (h1['Resisten_20'] - h1['Support_20']) / h1['Support_20']
        c_v22 = (
            (sideways_range <= 0.12)
            and (h0['Volume'] > h1['Volume'])
            and (h1['Close'] < h0['Close'])
            and (h0['Close'] > h0['MA_5'])
            and (h0['Value_Trx'] >= 5_000_000_000)
            and (h0['High'] / h1['Close'] >= 1.10)
        )
        if c_v22:
            triggered.append("V2.2 (Sideways Breakout)")

        if triggered:
            return {
                "Ticker"          : ticker,
                "Price"           : round(h0['Close'], 0),
                "Value (Billion)" : round(h0['Value_Trx'] / 1e9, 2),
                "Strategies"      : triggered,
            }

    except Exception:
        pass

    return None


# ============================================================
# UI & DRIVER UTAMA (STREAMLIT)
# ============================================================
st.sidebar.header("⚙️ Kontrol Pemindai")
max_workers = st.sidebar.slider(
    "Kecepatan Scan (Threads)", 5, 30, 15,
    help="Semakin tinggi semakin cepat, tapi bisa kena rate-limit yfinance."
)

# ------------------------------------------------------------
# FITUR AUDIT INVESTIGASI (MODUL BARU)
# ------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("🛠️ Investigasi Sinyal (Audit V1.1)")
debug_ticker = st.sidebar.text_input("Ketik Ticker (Contoh: BUMI)", "").upper().strip()

if debug_ticker:
    st.markdown(f"### 🛡️ Laporan Audit Kegagalan Data V1.1: **{debug_ticker}**")
    try:
        df_db = yf.Ticker(f"{debug_ticker}.JK").history(period="1y")
        if df_db.empty or len(df_db) < 10:
            st.error("❌ Data dari yfinance ampas! Ticker nggak ditemukan atau kosong.")
        else:
            df_db.index = df_db.index.tz_localize(None)
            df_db['MA_5'] = df_db['Close'].rolling(5).mean()
            df_db['Value_Trx'] = df_db['Close'] * df_db['Volume']
            
            h0 = df_db.iloc[-1]
            h1 = df_db.iloc[-2]
            
            audit_box = [
                {"Syarat Algoritma": "1. Volume Hari Ini > Kemarin", "Kondisi": h0['Volume'] > h1['Volume'], "Nilai Riil (yfinance)": f"{h0['Volume']:,} vs {h1['Volume']:,}"},
                {"Syarat Algoritma": "2. Close Hari Ini > Kemarin", "Kondisi": h0['Close'] > h1['Close'], "Nilai Riil (yfinance)": f"Rp {h0['Close']} vs Rp {h1['Close']}"},
                {"Syarat Algoritma": "3. Close Hari Ini > MA5 Hari Ini", "Kondisi": h0['Close'] > h0['MA_5'], "Nilai Riil (yfinance)": f"Rp {h0['Close']} vs MA5: {h0['MA_5']:.2f}"},
                {"Syarat Algoritma": "4. Value Transaksi Hari Ini >= 5 Miliar", "Kondisi": h0['Value_Trx'] >= 5_000_000_000, "Nilai Riil (yfinance)": f"Rp {h0['Value_Trx']/1e9:.3f} Miliar"},
                {"Syarat Algoritma": "5. Candle Kemarin Wajib Merah (Close < Open)", "Kondisi": h1['Close'] < h1['Open'], "Nilai Riil (yfinance)": f"C: {h1['Close']} | O: {h1['Open']}"},
                {"Syarat Algoritma": "6. Close Kemarin < MA5 Kemarin", "Kondisi": h1['Close'] < h1['MA_5'], "Nilai Riil (yfinance)": f"Rp {h1['Close']} vs MA5: {h1['MA_5']:.2f}"},
                {"Syarat Algoritma": "7. Candle Hari Ini Wajib Ijo (Close > Open)", "Kondisi": h0['Close'] > h0['Open'], "Nilai Riil (yfinance)": f"C: {h0['Close']} | O: {h0['Open']}"},
            ]
            
            df_audit = pd.DataFrame(audit_box)
            df_audit['Status Filter'] = df_audit['Kondisi'].apply(lambda x: "✅ TEMBUS" if x else "❌ REJECT")
            
            st.table(df_audit[["Syarat Algoritma", "Status Filter", "Nilai Riil (yfinance)"]])
            
            if df_audit['Kondisi'].all():
                st.success(f"Logika aman! Saham {debug_ticker} harusnya tembus radar screener utama.")
            else:
                st.warning(f"Kelebatan Sinyal Terbuka! Saham {debug_ticker} mental dari mesin karena status '❌ REJECT' di atas.")
    except Exception as e:
        st.error(f"Gagal mengecek data emiten: {e}")

# ------------------------------------------------------------
# CORE SCREENER ENGINE
# ------------------------------------------------------------
ALL_STRATEGIES = [
    "V1.1 (Reversal)",
    "V1.2 (Pullback)",
    "V1.3 (Continuation)",
    "V2.1 (Reversal)",
    "V2.2 (Sideways Breakout)",
    "BB Reversal",
    "BB MID",
    "MA 50 (Pullback)",
    "MA 200 (Pullback)",
]

st.markdown("---")
if st.button("🚀 MULAI PEMINDAIAN SELURUH SAHAM IDX (REAL-TIME)"):
    progress_bar = st.progress(0)
    status_text  = st.empty()
    results      = []
    total        = len(idx_tickers)

    status_text.markdown(f"**Memulai pemindaian paralel untuk {total} saham...**")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_single_stock, t): t for t in idx_tickers}

        for i, future in enumerate(as_completed(futures), start=1):
            res = future.result()
            if res:
                results.append(res)

            progress_bar.progress(i / total)
            if i % 20 == 0 or i == total:
                status_text.markdown(
                    f"🔄 Dipindai: **{i}/{total}** | Ditemukan: **{len(results)}** potensi"
                )

    status_text.success(f"🎉 Pemindaian selesai! Ditemukan **{len(results)}** saham potensial.")

    if results:
        df_all = pd.DataFrame(results)

        st.markdown("### 📊 Hasil Berdasarkan Strategi")
        st.info("💡 **Target Day Trading Yang Mulia:** TP1: 1-2% | TP2: 2-5% | TP3: 5-9% (Gunakan Trailing Stop)")
        
        tabs = st.tabs(ALL_STRATEGIES)

        for tab, strat in zip(tabs, ALL_STRATEGIES):
            with tab:
                filtered = df_all[
                    df_all['Strategies'].apply(lambda x: strat in x)
                ][["Ticker", "Price", "Value (Billion)"]].copy()

                if filtered.empty:
                    st.info(f"Tidak ada saham yang memicu **{strat}** hari ini.")
                else:
                    st.subheader(f"📈 {len(filtered)} saham masuk radar:")
                    st.dataframe(filtered, use_container_width=True)

                    csv = filtered.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label=f"📥 Download {strat}",
                        data=csv,
                        file_name=f"screener_{strat.replace(' ', '_').replace('/', '-')}.csv",
                        mime="text/csv",
                    )
    else:
        st.warning("Tidak ada saham yang lolos kriteria hari ini.")

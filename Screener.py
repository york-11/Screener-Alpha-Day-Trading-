import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# --- KONFIGURASI DASHBOARD ---
st.set_page_config(page_title="IDX Stock Screener", layout="wide")
st.title("🔍 IDX Quantitative Stock Screener V3.0")
st.markdown("Mesin Pemindai Sinyal Saham")

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
        stock = yf.Ticker(f"{ticker}.JK")
        df = stock.history(period="1y")
        
        if df.empty or len(df) < 200: # Diubah ke 200 karena kita butuh kalkulasi MA 200
            return None
        
        df.index = df.index.tz_localize(None)

        # Hitung Indikator Dasar
        df['SMA_5'] = df['Close'].rolling(window=5).mean()
        df['Value_Trx'] = df['Close'] * df['Volume']
        df['Resisten_20'] = df['High'].rolling(window=20).max()
        df['Support_20'] = df['Low'].rolling(window=20).min()
        df['MA_50'] = df['Close'].rolling(window=50).mean()
        df['MA_200'] = df['Close'].rolling(window=200).mean()
        
        # Bollinger Bands & EMA Tambahan (DIPERBAIKI DI SINI)
        df['BB_MID'] = df['Close'].rolling(window=20).mean()
        df['STD_20'] = df['Close'].rolling(window=20).std()
        df['BB_LOWER'] = df['BB_MID'] - (2 * df['STD_20'])
        df['BB_UPPER'] = df['BB_MID'] + (2 * df['STD_20'])
        df['BB_BANDWIDTH'] = (df['BB_UPPER'] - df['BB_LOWER']) / df['BB_MID']
        
        df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()

        # Ambil baris TERAKHIR 
        h0 = df.iloc[-1]
        h1 = df.iloc[-2]
        h2 = df.iloc[-3]
        h3 = df.iloc[-4]

        triggered_strategies = []

        # ==========================================
        # 1. Rumus V1.1 (Reversal)
        # ==========================================
        c_11_1 = h0['Volume'] > h1['Volume']
        c_11_2 = h1['Close'] < h1['SMA_5']
        c_11_3 = h1['Close'] < h1['Open']
        c_11_4 = h0['Close'] > h0['SMA_5']
        c_11_5 = h0['Value_Trx'] > 5_000_000_000
        if c_11_1 and c_11_2 and c_11_3 and c_11_4 and c_11_5:
            triggered_strategies.append("V1.1 (Reversal)")

        # ==========================================
        # 2. Rumus V1.2 (Pullback)
        # ==========================================
        c_12_1 = h1['High'] > (h1['SMA_5'] * 1.10)
        c_12_2 = h1['Close'] >= h1['Open']
        c_12_3 = (h0['Close'] >= h0['SMA_5']) and (h0['Close'] <= h0['SMA_5'] * 1.05)
        c_12_4 = h0['Open'] > h0['Close']
        c_12_5 = h0['Value_Trx'] > 1_000_000_000

        if c_12_1 and c_12_2 and c_12_3 and c_12_4 and c_12_5:
            triggered_strategies.append("V1.2 (Pullback)")
       

        # ==========================================
        # 3. Rumus V1.3 (Saham Super/continuation)
        # ==========================================
        c_13_1 = h0['Volume'] > h1['Volume']
        c_13_2 = h0['Close'] > h1['Close']
        c_13_3 = h0['Close'] > h0['SMA_5']
        c_13_4 = h0['Value_Trx'] > 5_000_000_000

        if c_13_1 and c_13_2 and c_13_3 and c_13_4:
            triggered_strategies.append("V1.3 (Breakout Resisten/Continuation)")

        # ==========================================
        # 4. Rumus V2.1 (Reversal)
        # ==========================================
        c_21_1 = h0['Volume'] > h1['Volume']
        c_21_2 = h0['Close'] > h1['Close']
        c_21_3 = h0['Close'] > h0['SMA_5']
        c_21_4 = h0['Value_Trx'] > 5_000_000_000
        c_21_5 = (h0['High'] / h1['Close']) >= 1.10
        c_21_6 = h1['Close'] < h1['SMA_5']
        c_21_7 = (h0['Close'] - h0['Open']) / h0['Open'] >= 0.10

        if c_21_1 and c_21_2 and c_21_3 and c_21_4 and c_21_5 and c_21_6 and c_21_7:
            triggered_strategies.append("V2.1 (Reversal)")

        # ==========================================
        # 5. Rumus V2.2 (Sideways Breakout)
        # ==========================================
        c_22_1 = ((h1['Resisten_20'] - h1['Support_20']) / h1['Support_20']) <= 0.15
        c_22_2 = h0['Close'] > h1['Resisten_20']
        c_22_3 = (h0['Close'] - h0['SMA_5']) / h0['SMA_5'] >= 0.10
        c_22_4 = h0['Volume'] > h1['Volume']
        c_22_5 = h0['Close'] > h1['Close']
        c_22_6 = h0['Close'] > h0['SMA_5']
        c_22_7 = h0['Value_Trx'] > 5_000_000_000
        c_22_8 = (h0['High'] / h1['Close']) >= 1.10

        if c_22_1 and c_22_2 and c_22_3 and c_22_4 and c_22_5 and c_22_6 and c_22_7 and c_22_8:
            triggered_strategies.append("V2.2 (Sideways Breakout)")
        
        # ==========================================
        # 6. Rumus BB MID (First Touch Pullback)
        # ==========================================
        c_mid_1 = (h0['Close'] > h0['BB_MID']) and (h0['Close'] <= h0['BB_MID'] * 1.02)
        c_mid_2 = h0['Value_Trx'] > 1_000_000_000
        c_mid_3 = (h0['EMA_10'] > h0['EMA_20']) and (h0['EMA_20'] > h0['EMA_50'])
        c_mid_4 = h0['BB_BANDWIDTH'] >= 0.10
        
        if c_mid_1 and c_mid_2 and c_mid_3 and c_mid_4:
            triggered_strategies.append("Bollinger Bands MID")

        # ==========================================
        # 7. Bollinger Bands Reversal
        # ==========================================
        c_bb_1 = h1['Low'] < h1['BB_Lower']
        c_bb_2 = h1['Close'] < h1['BB_Lower']
        c_bb_3 = h0['Close'] > h0['BB_Lower']
        c_bb_4 = h0['Value_Trx'] > 1_000_000_000
        c_bb_5 = h0['Volume'] > h1['Volume']
        c_bb_6 = h0['High'] > h1['High']
        c_bb_7 = h0['Close'] > h1['Close']

        if c_bb_1 and c_bb_2 and c_bb_3 and c_bb_4 and c_bb_5 and c_bb_6 and c_bb_7:
            triggered_strategies.append("BB Reversal")

        # Hitung Prev LLV(Low, 5) 
        prev_llv_low_5 = df['Low'].iloc[-6:-1].min()

        # ==========================================
        # 8. MA 50 Pullback - SINKRONISASI NAMA
        # ==========================================
        c_ma50_1 = prev_llv_low_5 > h0['MA_50']
        c_ma50_2 = h0['MA_50'] > h1['MA_50']
        c_ma50_3 = (h0['Low'] <= h0['MA_50'] * 1.02) and (h0['Close'] >= h0['MA_50'])
        c_ma50_4 = h0['Value_Trx'] > 1_000_000_000
        c_ma50_5 = h0['MA_50'] > h0['MA_200']
        
        if c_ma50_1 and c_ma50_2 and c_ma50_3 and c_ma50_4 and c_ma50_5:
            triggered_strategies.append("MA 50 (Pullback)")

        # ==========================================
        # 9. MA 200 Pullback - SINKRONISASI NAMA
        # ==========================================
        c_ma200_1 = prev_llv_low_5 > h0['MA_200']
        c_ma200_2 = h0['MA_200'] > h1['MA_200'] 
        c_ma200_3 = (h0['Low'] <= h0['MA_200'] * 1.02) and (h0['Close'] >= h0['MA_200'])
        c_ma200_4 = h0['Value_Trx'] > 1_000_000_000
        c_ma200_5 = h0['MA_50'] > h0['MA_200'] 
        
        if c_ma200_1 and c_ma200_2 and c_ma200_3 and c_ma200_4 and c_ma200_5:
            triggered_strategies.append("MA 200 (Pullback)")

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
max_workers = st.sidebar.slider("Kecepatan Scan (Threads)", 5, 30, 15, help="Semakin tinggi semakin cepat.")

if st.button("🚀 MULAI PEMINDAIAN SELURUH SAHAM IDX (REAL-TIME)"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    total_saham = len(idx_tickers)
    
    status_text.markdown(f"**Memulai pemindaian paralel untuk {total_saham} saham...**")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_single_stock, ticker): ticker for ticker in idx_tickers}
        
        for i, future in enumerate(futures):
            res = future.result()
            if res:
                results.append(res)
            
            progress = (i + 1) / total_saham
            progress_bar.progress(progress)
            if i % 20 == 0:
                status_text.markdown(f"🔄 Dipindai: {i+1}/{total_saham} Saham | Ditemukan: {len(results)} potensi")
                
    status_text.success(f"🎉 Pemindaian Selesai! Menemukan {len(results)} saham potensial hari ini.")
    
    if results:
        df_all = pd.DataFrame(results)
        
        all_strategies = [
            "V1.1 (Reversal)",
            "V1.2 (Pullback)",
            "V1.3 (Breakout Resisten/Continuation)",
            "V2.1 (Reversal)",
            "V2.2 (Sideways Breakout)",
            "Bollinger Bands MID",
            "Bollinger Bands Reversal",
            "MA 50 (Pullback)",
            "MA 200 (Pullback)"
        ]
        
        st.markdown("### 📊 Hasil Berdasarkan Strategi")
        tabs = st.tabs(all_strategies)
        
        for idx, strat in enumerate(all_strategies):
            with tabs[idx]:
                filtered_df = df_all[df_all['Strategies'].apply(lambda x: strat in x)].copy()
                
                if filtered_df.empty:
                    st.info(f"Tidak ada saham yang memicu rumus **{strat}** pada hari ini.")
                else:
                    display_df = filtered_df[["Ticker", "Price", "Value (Billion)"]]
                    st.subheader(f"📈 {len(display_df)} Saham terdeteksi masuk radar:")
                    st.dataframe(display_df, use_container_width=True)
                    
                    csv = display_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label=f"📥 Download Daftar {strat}",
                        data=csv,
                        file_name=f"screener_{strat.split(' ')[0]}.csv",
                        mime='text/csv',
                    )
    else:
        st.warning("Hari ini tidak ada satu pun saham di IDX yang lolos semua kriteria rumus teknikal di atas.")

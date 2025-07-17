
import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta

st.set_page_config(page_title="فلترة الأسهم", layout="centered")
st.title("📊 فلتر الأسهم الأمريكية والسعودية")

uploaded_file = st.file_uploader("📥 ارفع ملف الأسهم (Excel بصيغة stocks.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        usa_symbols = pd.read_excel(uploaded_file, sheet_name="USA")["Ticker"].dropna().tolist()
        sa_symbols = pd.read_excel(uploaded_file, sheet_name="SAUDI")["Ticker"].dropna().tolist()
        all_symbols = usa_symbols + sa_symbols

        st.info(f"📈 عدد الأسهم: {len(all_symbols)}")

        progress = st.progress(0)
        qualified_stocks = []

        for idx, symbol in enumerate(all_symbols):
            try:
                df = yf.download(symbol, period="6mo", interval="1d", progress=False)
                if len(df) < 50:
                    continue

                df["ema7"] = ta.ema(df["Close"], length=7)
                df["ema20"] = ta.ema(df["Close"], length=20)
                df["ema50"] = ta.ema(df["Close"], length=50)
                df["rsi"] = ta.rsi(df["Close"], length=14)
                df["roc"] = ta.roc(df["Close"], length=12)

                latest = df.iloc[-1]

                if (
                    latest["Close"] > latest["ema7"]
                    and latest["ema7"] > latest["ema20"]
                    and latest["ema20"] > latest["ema50"]
                    and latest["rsi"] > 50
                    and latest["roc"] > 0
                ):
                    qualified_stocks.append(symbol)
            except:
                continue

            progress.progress((idx + 1) / len(all_symbols))

        st.success(f"✅ عدد الأسهم المطابقة: {len(qualified_stocks)}")
        st.dataframe(pd.DataFrame(qualified_stocks, columns=["الأسهم المطابقة"]))

        csv = pd.DataFrame(qualified_stocks, columns=["الأسهم المطابقة"]).to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ تحميل النتائج كـ CSV", data=csv, file_name="filtered_stocks.csv", mime="text/csv")

    except Exception as e:
        st.error(f"حدث خطأ في الملف: {e}")
else:
    st.warning("🔺 الرجاء رفع ملف Excel فيه ورقتين: 'USA' و 'SAUDI'")

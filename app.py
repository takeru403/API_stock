import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('就活株価可視化アプリ')

st.sidebar.write("""
# 就活可視化
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""
## 表示日数選択
""")

#スライダーで読み込んだ日付をdaysに引き渡される
days =st.sidebar.slider("日数",1,20,10)

st.write(f"""
### 過去 **{days}日間** の就活する会社の株価
""")

#データを毎回撮ってくる(API)などは素早くデータをとってくることができる。
@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try: 
    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    #株価の上限と下限を設定する。
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0.0, 3200.0, (0.0, 3200.0)
    )

    tickers = {
        '東海東京フィナンシャルホールディングス': '8616.T',
        'SBIホールディングス': '8473.T',
        '岡三證券': '8609.T',
        '(株)日本取引所グループ': '8697.T',
        '三菱UFJフィナンシャルグループ': '8306.T',
    }
    df = get_data(days, tickers)
    companies = st.multiselect(
        '会社名を選択してください。',
        list(df.index),
        ['東海東京フィナンシャルホールディングス', 'SBIホールディングス', '岡三證券', '(株)日本取引所グループ','三菱UFJフィナンシャルグループ']
    )

    if not companies:
        st.error('少なくとも一社は選んでください。')
    else:
        data = df.loc[companies]
        st.write("### 株価", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': '株価'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("株価:Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "おっと！なにかエラーが起きているようです。"
    )
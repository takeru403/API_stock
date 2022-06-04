import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

st.title("streamlit 超入門")

st.write("DataFrame")

df = pd.DataFrame({
    '一列目':[1,2,3,4],
    '二列目':[10,20,30,40]
})

#これによって最大値にハイライトが付くようになった。
#jsonも載せることができる。
st.dataframe(df.style.highlight_max(axis=0))
#staticなdataframeを作るときはtable

#マジックコマンド markdownや、latexや、コードを書くことができる。
"""
# 章
## 節

```python 
import streamlit as st
import numpy as np
import pandas as pd

```
"""

#チャートを書く
# df_chart = pd.DataFrame(
#     np.random.rand(20,3),
#     columns=["a","b","c"]
# )
# #折れ線グラフで表示
# st.line_chart(df_chart)
# #棒グラフ
# st.bar_chart(df_chart)
# #ヒストグラム
# fig,ax = plt.subplots()
# st.pyplot(df_chart)
# #散布図
# st.altair_chart()

#インタラクティブな操作
#if st.checkbox():
    #ここにチェックボックスを入れる操作を加える。
    #サイドバー？

option = st.selectbox(
    'あなたの好きな数字を教えてください',
    list(range(1,11))
)

'あなたの好きな数字は', option, "です"

#サイドバーにするには、　st.sidebar.〜〜 で作ることができる。
st.sidebar.text_input("こんにちは")

#カラムに関するもの
left_column, right_column = st.beta_columns(2)
button = left_column.button("右カラムに文字w表示")
if button:
    right_column.write("ここは右カラム")

#エクスパンダー
expander = st.beta_expander("問い合わせ")
expander.write("お問い合わせ内容を書く")


latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.te(f'Iteration {i + 1}')
    bar.progress(i + 1)
    time.sleep(0.1)

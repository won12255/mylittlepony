import streamlit as st
import pandas as pd
import altair as alt

# 페이지 제목 설정
st.title('국방예산, 조국수호의 나침반')
st.markdown("---")

# 데이터 로드
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path, encoding='euc-kr')
    return df

df_original = load_data('국방예산추이_20250906112036.csv')

# 데이터 전처리 및 시각화 준비
df_filtered = df_original[df_original['특성별(1)'] == '국방비 (억원)'].drop(columns=['특성별(1)'])
df_filtered = df_filtered.rename(columns={'특성별(2)': '항목'})

# '총액' 데이터 제외
df_filtered = df_filtered[df_filtered['항목'] != '총액']

# 연도 선택 슬라이더
st.sidebar.header('연도 선택')
selected_year = st.sidebar.slider(
    '연도를 선택하세요',
    min_value=2020,
    max_value=2024,
    step=1
)

st.header('연도별 국방 예산 추이')
st.markdown(f"**선택된 연도: {selected_year}년**")

# 데이터 변환
df_melted = df_filtered.melt(id_vars='항목', var_name='연도', value_name='예산')
df_melted['연도'] = df_melted['연도'].astype(int)

# 선 그래프 생성
line_chart = alt.Chart(df_melted).mark_line(point=True).encode(
    x=alt.X('연도:O', title='연도'),
    y=alt.Y('예산', title='예산 (억 원)', axis=alt.Axis(format='~s')),
    color=alt.Color('항목', title='예산 항목'),
    tooltip=[
        alt.Tooltip('연도', title='연도'),
        alt.Tooltip('항목', title='항목'),
        alt.Tooltip('예산', title='예산', format=',.0f')
    ]
).properties(
    title='국방 예산(전력운영비, 방위력개선비) 추이'
).interactive()

st.altair_chart(line_chart, use_container_width=True)

# 선택된 연도 데이터 강조
st.subheader(f"{selected_year}년 국방 예산 상세")
df_selected_year = df_filtered[['항목', str(selected_year)]].rename(columns={str(selected_year): '예산 (억원)'})
st.table(df_selected_year.set_index('항목'))

st.markdown("---")
st.markdown("""
<div style="text-align: center; font-size: 14px; color: #888;">
    데이터 출처: 국방부
</div>
""", unsafe_allow_html=True)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 폰트 설정
font_location = 'C:/Windows/Fonts/malgun.ttf' # For Windows
font_name = fm.FontProperties(fname=font_location).get_name()
plt.rc('font', family=font_name)

df = pd.read_csv(r'C:\Users\grace\Downloads\서울특별시_전동킥보드_견인_현황_20230831.csv', sep=',', low_memory=False, encoding='cp949')

# df = df[df['유형'].str.contains('점자블록', na=False)]
df = df[['번호', '신고일', '구정보', '주소', '유형', '조치일']]

df['번호'] = pd.to_numeric(df['번호'])
df = df.sort_values(by='번호', ascending=True)

df.columns = ['num', 'declare', 'gu', 'address', 'type', 'clear']

top8 = df['type'].value_counts().head(8)

plt.figure(figsize=(10, 8))
top8.plot(kind='bar')
plt.title('서울특별시 전동킥보드 견인유형 Top 8')
plt.xlabel('Type')
plt.ylabel('Count')
plt.show()

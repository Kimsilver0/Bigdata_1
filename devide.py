import pandas as pd
import numpy as np

df = pd.read_csv(r'C:\Users\grace\Downloads\서울특별시_전동킥보드_견인_현황_20230831.csv', sep=',', low_memory=False, encoding='cp949')

# '유형' 칼럼에서 '점자블록'을 포함하고 있는 모든 행 선택
df = df[df['유형'].str.contains('점자블록', na=False)]

df = df[['번호', '신고일', '구정보', '주소', '유형', '조치일']]

# '번호' 칼럼을 숫자로 변환하고, 그 값을 기준으로 오름차순 정렬
df['번호'] = pd.to_numeric(df['번호'])
df = df.sort_values(by='번호', ascending=True)

# 칼럼명 단순화
df.columns = ['num', 'declare', 'gu', 'address', 'type', 'clear']

# DataFrame을 새로운 CSV 파일로 저장
df.to_csv(r'C:\Users\grace\Downloads\서울특별시_전동킥보드_견인_현황_정렬.csv', index=False, encoding='utf-8-sig')

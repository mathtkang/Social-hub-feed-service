import sys
import os
import pandas as pd


# 현재 스크립트 디렉토리를 Python 경로에 추가
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

from posts.models import Posts


# CSV 파일 경로 설정
csv_file = '../load_data/dummy_data.csv'

# CSV 파일 읽기
df = pd.read_csv(csv_file)

# 각 행을 순회하며 데이터베이스에 저장
for index, row in df.iterrows():
    post = Posts(
        content_id=row['content_id'],
        type=row['type'],
        title=row['title'],  # CSV 파일에는 'title' 필드가 없는데 모델에는 'title' 필드가 있어 추가함
        content=row['content'],
        view_count=row['view_count'],
        like_count=row['like_count'],
        share_count=row['share_count'],
    )
    post.save()

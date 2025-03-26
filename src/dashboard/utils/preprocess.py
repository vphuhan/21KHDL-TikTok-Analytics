import pandas as pd
import ast
from config import COLUMN_LABELS
import numpy as np


# def parse_list_column(value):
#     try:
#         parsed = ast.literal_eval(value) if isinstance(
#             value, str) and value.startswith('[') else value
#         return parsed if isinstance(parsed, list) else [parsed]
#     except:
#         return [value]


def load_data(path):
    # df = pd.read_csv(path)
    df = pd.read_parquet(path)
    # list_columns = list(COLUMN_LABELS.keys())  # từ config
    # for col in list_columns:
    #     if col in df.columns:
    #         df[col] = df[col].apply(parse_list_column)
    # loại "Audio không liên quan ẩm thực"
    df = df[~df['categories'].apply(lambda x: isinstance(
        x, list) and "Không liên quan ẩm thực" in x)]
    # df['categories'] = df['categories'].apply(
    #     lambda x: list(x) if isinstance(
    #         x, (list, np.ndarray, pd.Series)) else ([] if pd.isna(x) else [x])
    # )

    # # Sau đó lọc an toàn
    # df = df[~df['categories'].apply(lambda x: "Không liên quan ẩm thực" in x)]
    # lambda x: "Không liên quan ẩm thực" in x if isinstance(x, list) else False)]

    # df[['has_personal_story', 'has_cta']] = df[[
    #     'has_personal_story', 'has_cta']].astype('bool')
    # print(df.info())
    df['engagement_rate'] = (df['statsV2.diggCount']+df['statsV2.commentCount'] +
                             df['statsV2.shareCount']+df['statsV2.collectCount']) / (df['statsV2.playCount'] + 1e-6)
    df.loc[df['statsV2.playCount'] < 1, 'engagement_rate'] = 0

    return df

def apply_filters(df, selected_metric):
    metric_map = {
        "Views": "statsV2.playCount",
        "Likes": "statsV2.diggCount",
        "Comments": "statsV2.commentCount",
        "Shares": "statsV2.shareCount",
    }
    metric_col = metric_map[selected_metric]
    return df[metric_col]

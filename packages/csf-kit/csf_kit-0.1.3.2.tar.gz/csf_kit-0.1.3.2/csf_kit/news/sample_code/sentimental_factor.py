# encoding=utf8

import pandas as pd
from csf_kit.news.util import extract_senti_info_from_file
from csf_kit.news.util import extract_tag_info_from_file
from csf_kit.news.util import extract_data_from_files
from csf_kit.news.util import align_trade_date


def extract_senti_data_from_file(file_path):

    """extract_senti_data"""

    print(file_path)

    df_tag = extract_tag_info_from_file(file_path,
                                        news_filed=['newsId', 'newsTs'],
                                        tag_type='Company',
                                        tag_filed=['ItemExtId', 'ItemRelevance'],
                                        df=True)

    df_senti = extract_senti_info_from_file(file_path,
                                            news_filed=['newsId'],
                                            senti_type=['Company'],
                                            senti_filed=['entityCode', 'emotionIndicator', 'emotionWeight'],
                                            df=True
                                            )

    df_tag.columns = df_tag.columns.map({'newsId': 'news_id',
                                         'newsTs': 'news_time',
                                         'ItemExtId': 'sec_code',
                                         'ItemRelevance': 'relevance'
                                         })

    df_senti.columns = df_senti.columns.map({'newsId': 'news_id',
                                             'entityCode': 'sec_code',
                                             'emotionIndicator': 'senti_type',
                                             'emotionWeight': 'senti_weight'
                                             })

    df_merge = pd.merge(df_senti, df_tag, how='left')
    sec_code_split = df_merge['sec_code'].str.split('_')

    mask = (sec_code_split.str[0].str[0].isin(['0', '3', '6']))\
           & (sec_code_split.str[-2].isin(['SH', 'SZ']))\
           & (sec_code_split.str[-1] == 'EQ')

    df_merge = df_merge[mask]
    df_merge.loc[:, 'news_time'] = df_merge.loc[:, 'news_time'].str.split('+').str[0]
    df_merge.loc[:, 'news_time'] = pd.to_datetime(df_merge['news_time'])

    return df_merge.reset_index(drop=True)


def extract_senti_data_from_files(folder_path):

    senti_raw = extract_data_from_files(folder_path, extract_senti_data_from_file)

    return senti_raw


def raw_senti_data_process(df_raw, cut_hour=15, cut_minute=0):
    """
    process raw data loaded by function load_news_files:
    1. change senti_type: 2 --> -1
    2. calculate senti_score: senti_score = senti_type*senti_weight*100
    3. map calendar date to trade date
    """
    df_raw['senti_type'] = df_raw['senti_type'].replace(2, -1)
    df_raw['senti_score'] = df_raw['senti_type'] * df_raw['senti_weight'] * 100
    df_raw['senti_score_rel'] = df_raw['senti_score'] * df_raw['relevance']
    df_raw['sec_code'] = [''.join([i[0:6], '.XSHE']) if i[-5:-3] == 'SZ' else ''.join([i[0:6], '.XSHG']) for i in
                      df_raw['sec_code']]

    df_aligned = align_trade_date(df_raw, date_col='news_time', cut_hour=cut_hour, cut_minute=cut_minute)

    return df_aligned


def sentiment_factor_calc(senti_score,
                          use_rel_score=True,
                          cal_tot_score=False,
                          ex_neutral=True,
                          score_diff=False,
                          mean_type='sma'
                          ):
    """

    :param senti_score:
    :param use_rel_score: Bool, default True. Set False to use 'senti_score', otherwise use 'senti_score_rel'
    :param cal_tot_score: Bool, default False. Set True to calculate daily total sentiment score for each stock, otherwise
                          calculate mean sentiment score.
    :param ex_neutral: Bool, default True. Set False to keep the neutral
    :param score_diff: Bool, defa
    :param mean_type:
    :return:
    """


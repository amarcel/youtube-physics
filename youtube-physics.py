from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns; sns.set(style='white')
import numpy as np
import json
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import pearsonr

api_key = 'YOUR_YOUTUBE_API_KEY'

channel_ids = [ 'UCVrCCRwhnXWl1-ulZPUIpmw',
                'UCNlkXScvDUJrGbN1r7jQbUA',
                'UCkRpTBmo09y3QfU35oqWtmw',
                'UCzshJ2mSjxhqKFBUXqP49Uw',
                'UC_e7B1w8T-4ZD-QtIVAO9pg',
                'UChcAczGVMrjZ7cCTgpVYXRQ',
                'UCmiptCNi7GR1P0H6bp9y0lQ',
                'UCSdrRq5JGx2U0jAFjmKF0aA',
                'UCV8ZgEjwdNnZC4_FJtdDFCg',
                'UCHGUyE738ID1Up9rhaBYC1g',
                'UCHW95H66qwKrZVizKOk1BJA',
                'UC1lUEcHrQwbusC5ext1himg',
                'UCF5qm-yrOeDq1sSmE-gCh0w',
                'UC4iI8T1vfJuLDnHlAzBta1g',
                'UCThYOehChjehTM5bvBB9iAA',
                'UC0soG5i-H5ULQqpAluWbxjQ',
                'UCFIsRGd-TL4mp35x4nq5COw',
                'UCEGnXcwKgyZlUtyY3bN_-0g',
                'UCgl3Vrk6QkhQ58af8bJozEA',
                'UC3XaOhe6PsVc68KQ6neILZQ',
                'UCXu_DlgwRl1ZhTf721VyaWQ',
                'UCxPNyWlm0HQ4sHZWzY-ObOw',
                'UC5kH64r2GvqP4OzExx7Ymfw',
                'UCktbwZM-Q_IfrZMmFimmzYA',
                'UC4sA8H77_Fq2DZCpPzQkcGw',
                'UCAXw5itzS572yhew-Z7s9XA',
                'UCI1yl8sszRCR9gfN9d-8Wsg',
                'UCVVB_obmDDitoFVpDu-VdKA',
                'UCcMFaCVv3BP78E_4TGLOKIw',
                'UCFYdMYfSDRgdbshthxHxmlQ',
                'UCI9cd21kVICTr6pdS_tLvtg',
                'UCyTOJBJhIQTJOLU9ENU95GA',
                'UC_MFYf4kVS6-4GZhKE5lHGA',
                'UCNmszw8n56iFYjSfLSzsMhg',
                'UCOF7MPJutCPGFGp-qP2s1Qg',
                'UC-uhnhzjNrvK0qKZfdLtnzw',
                'UCh4BXwKCJpDOG_g123Unsrg',
                'UCKWelzjqzIkfDo4IMYgrEtQ',
                'UCUwc8Mchmm82TNLutPUOkNA',
                'UCeeoKtZLDRvYLLsQGxll2YQ',
                'UCxPaZqwYIAojfZ-D_60MDuQ',
                'UCiBDWKbSUxCeZxs3OBqFKZg',
                'UCtw3XwOO8t76Ns0M5kJJ09g',
                'UCjlPDa70bjRMiVx1X1BdMDg',
                'UC7QYaiwlsOjkEjCLkyE1njw',
                'UC9_o33xRStjrlca52wzBK7w',
                'UCrB_peu2vvXllnIbsNubzaA',
                'UCfN62ZJrRj5-t3UxbSRHKoA',
                'UCbfpYGPzXf1QjakNd-hpfcw',
                'UC6lrmWd3ARFmLKz35su8Uuw',
              ]

youtube = build('youtube', 'v3', developerKey=api_key)

def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
                part='snippet,contentDetails,statistics',
                id= ','.join(channel_ids)
    )
    response = request.execute()
    for i in range(len(response['items'])):
        data = dict(
                Channel_name = response['items'][i]['snippet']['title'],
                Custom_url = response['items'][i]['snippet']['customUrl'],
                Subscribers = response['items'][i]['statistics']['subscriberCount'],
                Views = response['items'][i]['statistics']['viewCount'],
                Total_Videos = response['items'][i]['statistics']['videoCount'],
                Playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
        )
        all_data.append(data)
    return all_data

channel_stats = get_channel_stats(youtube, channel_ids)
print(channel_stats)

channel_data = pd.DataFrame(channel_stats)

channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
channel_data['Views'] = pd.to_numeric(channel_data['Views'])
channel_data['Total_Videos'] = pd.to_numeric(channel_data['Total_Videos'])

channel_data = channel_data.sort_values(by='Subscribers', ascending=False)
channel_data

channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
channel_data['Views'] = pd.to_numeric(channel_data['Views'])
channel_data['Total_Videos'] = pd.to_numeric(channel_data['Total_Videos'])
channel_data.dtypes

def calc_index_performance(subs, videos, views, md_subs, md_videos, md_views):
  return (subs * videos * views) / (md_subs * md_videos * md_views)

md_subs = channel_data['Subscribers'].median()
md_videos = channel_data['Total_Videos'].median()
md_views = channel_data['Views'].median()

channel_data['Index_Performance'] = calc_index_performance(channel_data['Subscribers'], channel_data['Total_Videos'], channel_data['Views'], md_subs, md_videos, md_views)
channel_data['Index_Performance_log10'] = np.log10(channel_data['Index_Performance'])
channel_data

channel_data.describe().apply(lambda s: s.apply('{0:.2f}'.format))

df_boxplot_chann = channel_data[['Subscribers', 'Views', 'Total_Videos', 'Index_Performance_log10']]
fig,axes = plt.subplots(2,2,figsize = (8,4))
sns.set_style('darkgrid')

for ax, feature in zip(axes.flatten(), df_boxplot_chann.columns):
  sns.boxplot(data=df_boxplot_chann, x=feature, ax=ax)
  if feature == 'Subscribers': feature = 'Subscribers'
  elif feature == 'Views': feature = 'Views'
  elif feature == 'Total_Videos': feature = 'Total number of videos'
  elif feature == 'Index_Performance_log10': feature = 'Performance index'
  ax.set_title(f'Boxplot {feature}')
  ax.xaxis.set_label_text(feature)
  ax.yaxis.grid(True)

plt.tight_layout()
plt.show()

def corrfunc(x, y, ax=None, **kws):
    # """Plot the correlation coefficient in the top left hand corner of a plot."""
    r, _ = pearsonr(x, y)
    ax = ax or plt.gca()
    ax.annotate(f'R² = {r:.2f}', xy=(.4, .9), xycoords=ax.transAxes)

channel_data_corr = channel_data[['Subscribers', 'Views', 'Total_Videos', 'Index_Performance_log10']]

# Renaming columns
channel_data_corr.rename(columns={'Subscribers': 'Inscritos', 'Views': 'Visualizações', 'Total_Videos': 'Vídeos', 'Index_Performance_log10': 'Índice de performance'}, inplace=True)
g = sns.pairplot(data=channel_data_corr, kind='reg', corner=True, plot_kws={'line_kws':{'color':'red'}})
g.map_lower(corrfunc)
plt.show()

# Channels' analysis:
channel_name = 'Professor Boaro' # change for others channels' names
playlist_id = channel_data.loc[channel_data['Channel_name'] == channel_name, 'Playlist_id'].iloc[0]
playlist_id

def get_video_ids(youtube, playlist_id):
    request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId = playlist_id,
                maxResults=50)
    response = request.execute()
    video_ids = []
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    more_pages = True

    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                        part='contentDetails',
                        playlistId = playlist_id,
                        maxResults=50,
                        pageToken = next_page_token
            )
            response = request.execute()

            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')

    return video_ids

video_ids = get_video_ids(youtube, playlist_id)

def get_video_details(youtube, video_ids):
    all_video_stats = []
    for i in range (0, len(video_ids), 50):
        request = youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id= ','.join(video_ids[i:i+50]))
        response = request.execute()
        for video in response['items']:
          if parse_isoduration(video['contentDetails']['duration']) > 3*61:
            try:
              video_stats = dict(Title = video['snippet']['title'],
                                Published_date = video['snippet']['publishedAt'],
                                Views = video['statistics']['viewCount'],
                                Likes = video['statistics']['likeCount'])
            except:
              video_stats = dict(Title = video['snippet']['title'],
                                Published_date = video['snippet']['publishedAt'],
                                Views = video['statistics']['viewCount'],
                                Likes = 0)
            all_video_stats.append(video_stats)
    return all_video_stats

video_details = get_video_details(youtube, video_ids)

video_data = pd.DataFrame(video_details)
video_data.head(10)

video_data ['Published_date'] = pd.to_datetime(video_data ['Published_date']).dt.date
video_data ['Views'] = pd.to_numeric(video_data ['Views'])
video_data ['Likes'] = pd.to_numeric(video_data ['Likes'])
video_data

top10_videos_liked = video_data.sort_values(by='Likes', ascending=False).head(10)
top10_videos_liked

sns.barplot(x='Likes', y='Title', data=top10_videos_liked).set_title(channel_name).set_color('black')
plt.xlabel('Number of likes')
plt.ylabel('Video title')
plt.show()

video_data['Published_date'] = pd.to_datetime(video_data['Published_date'], infer_datetime_format=True)
top10_videos_liked_2024 = video_data[video_data['Published_date'].dt.year == 2024].sort_values(by='Likes', ascending=False).head(10)
top10_videos_liked_2024

ax1 = sns.barplot(x='Likes', y='Title', data=top10_videos_liked_2024).set_title(f'{channel_name} (2024 videos)').set_color('black')
plt.xlabel('Number of likes')
plt.ylabel('Video title')
plt.show()



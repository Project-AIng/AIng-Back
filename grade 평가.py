import tensorflow as tf
import matplotlib 
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow_hub as hub
#from matplotlib.patches import Polygon
import numpy as np
from math import pi
import seaborn as sns
df = pd.read_excel('/content/drive/MyDrive/Colab Notebooks/data/aingtest.xlsx')

    # 데이터 전처리
df = df[['date', 'stu_id', 'grammar', 'clarity', 'coherence', 'vocabulary','structure']]  # 필요한 컬럼들만 선택

df = df.sort_values(by=['date'])  # 날짜 순서대로 정렬



def df_init():
# 엑셀 파일에서 데이터 가져오기
    df = pd.read_excel('/content/drive/MyDrive/Colab Notebooks/data/aingtest.xlsx')
    # 데이터 전처리
    df = df[['date', 'stu_id', 'grammar', 'clarity', 'coherence', 'vocabulary','structure']]  # 필요한 컬럼들만 선택
    df = df.sort_values(by=['date'] )  # 날짜 순서대로 정렬
    return df

def all_average(df):
    all_scoring=[]
    gra_tscore = df['grammar'].mean()
    all_scoring.append(gra_tscore)
    cla_tscore = df['clarity'].mean()
    all_scoring.append(cla_tscore)
    coh_tscore = df['coherence'].mean()
    all_scoring.append(coh_tscore)
    voc_tscore = df['vocabulary'].mean()
    all_scoring.append(voc_tscore)
    str_tscore = df['structure'].mean()
    all_scoring.append(str_tscore)
    return all_scoring


def sort_id(df):
    sortid_df = df.loc[df['stu_id'] == stu_id]    
    return sortid_df


def calculate_score(df):
    #총점계산
    weights = [5, 4, 3, 2, 2] 
    scores = df['grammar', 'clarity', 'coherence', 'vocabulary', 'structure']
    total_weight = sum(weights)
    weighted_scores = [score * weight for score, weight in zip(scores, weights)]
    final_score = sum(weighted_scores) / total_weight
    return final_score


def plot_scores(df):
    stu_df = sort_id(df)
#마지막 시험본것만
#일단 오각형 그래프
    all_stuscores = all_average(df)
    stuscore_df = stu_df[['grammar', 'clarity', 'coherence', 'vocabulary', 'structure']]
    stuscore_df = stuscore_df[-1:]
    stuscore_df = stuscore_df.values.flatten().tolist()

    theta = ['Grammar', 'Clarity', 'Coherence', 'Vocabulary', 'Structure']

    angles = np.linspace(0, 2 * np.pi, len(theta), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10), subplot_kw=dict(polar=True))
    plt.title("Now Test Score", fontsize=20)
    plt.xticks(angles[:-1], theta, color='black', size=18)

    plt.yticks(np.arange(2, 11, 2), color='grey', size=14)
    plt.ylim(0, 10)

    ax.set_rlabel_position(0)

    ax.plot(angles, all_stuscores + [all_stuscores[0]], linewidth=1, linestyle='solid', label='all stu', color = 'lightpink')
    ax.fill(angles, all_stuscores + [all_stuscores[0]], 'lightpink', alpha=0.4)

    ax.plot(angles, stuscore_df + [stuscore_df[0]], linewidth=1, linestyle='solid', label=stu_id, color = 'skyblue')
    ax.fill(angles, stuscore_df + [stuscore_df[0]], 'skyblue', alpha=0.4)

    plt.legend(loc='upper right', bbox_to_anchor=(1.01, 1))

    plt.show()

def date_growth(df):
   dataset = ['grammar', 'clarity', 'coherence', 'vocabulary', 'structure']
   student_data = df[df['stu_id'] == stu_id].tail(10).reset_index(drop = True)
   
   for student_id in student_data['stu_id'].unique():
        sns.set_style("darkgrid")
   
   for col in dataset:
        sns.lineplot(x= np.arange(1,len(student_data)+1), y=student_data[col], label=col)
    
   plt.xticks(np.arange(1,len(student_data)+1),rotation=45)  
   plt.xlabel('About 10 Recent English Tests')
   plt.ylabel('Score')
   plt.legend(loc='upper right', bbox_to_anchor=(1.05, 1))
   plt.title('Student {} of English Score'.format(student_id))
   plt.show()  





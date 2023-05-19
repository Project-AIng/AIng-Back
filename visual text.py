import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import WordCloud
import tokenization



a ="""
Football, also known as soccer in some countries, is a beloved sport that brings people together from all walks of life. The roar of the crowd and the exhilaration of scoring a goal create an electric atmosphere in stadiums around the world. Players showcase their skills and teamwork, dribbling past opponents, executing precise passes, and unleashing powerful shots. The competitive nature of the game fosters a sense of camaraderie and sportsmanship among players. Whether it's the FIFA World Cup or local league matches, football unites fans, ignites passions, and leaves lasting memories for both players and spectators alike
""" 
document_column = "select subject" #여기서 select subject는 사용자가 선택한 주제

def visual_words(text):
    
    document_column = "select subject" #여기서 select subject는 사용자가 선택한 주제 사용자 분석시 모든 대화결과 들어가야함
    text = pd.Series(text.lower().split())
    word_lengths = text.apply(len)
    long_words = text[word_lengths >= 6]

    num_words_to_visualize = 100
    wordcloud = WordCloud(width=800, height=400, max_words=num_words_to_visualize, background_color='white').generate_from_frequencies(long_words.value_counts())
    word_counts = text.value_counts()
    word_counts = word_counts[word_counts.index.str.len()>=6].sort_values(ascending=False)

    num_words_to_visualize = 20
# display the wordcloud
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Top {num_words_to_visualize} Most Frequent Words in {document_column} (6+ Characters)')
    #plt.savefig('figure1.png')  # 그림을 이미지 파일로 저장
    plt.show()

visual_words(a)



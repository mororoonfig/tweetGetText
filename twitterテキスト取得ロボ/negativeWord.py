# TODO
# ネガティブワードをリスト化
# (15分起きに)取得したツイートの単語頻度解析をする
# ネガティイブワードにない言葉は係り受け係り受け解析でスコア化
# ネガティブスコアと単語頻度をかけた結果がトレンドに
# 各トレンドで一番ネガティブなツイートを固定
import pandas as pd
import janome
import jaconv
import getWord

from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *

# 極性辞書
word_Data = pd.read_csv("C:/Users/hm111/twitterテキスト取得ロボ/NPWord/wordScore.csv", encoding='cp932')
# スコアが以下のデータのみ
word_Data = word_Data[word_Data["スコア"] <= 0]
# jaconvを使って読み仮名を全てカタカナに変換
word_Data['読み'] = word_Data['読み'].apply(lambda x: jaconv.hira2kata(x))
# なぜか読みや品詞まで同じなのに、異なるスコアが割り当てられていたものがあったので重複を削除
word_Data = word_Data[~word_Data[['基本形', '読み', '品詞']].duplicated()]

# 取得テキスト
get_Word = getWord.df["text"]
# データ型変換(Series→List)
get_Word_list = get_Word.to_list()
# リストのワード連結
words = "。".join(get_Word_list)

# 形態素解析オブジェクトの生成
t = Tokenizer()
# テキストを一行ずつ処理
word_txt = {}
lines = words.split("\r\n")
for line in lines:
    malist = t.tokenize(line)
    for w in malist:
        word = w.surface  # 単語情報の読込
        ps = w.part_of_speech  # 品詞情報の読込
        if ps.find('名詞') < 0:
            continue  # 名詞のカウント
        if not word in word_txt:
            word_txt[word] = 0
        word_txt[word] += 1  # カウント
# 頻出単語の表示
keys = sorted(word_txt.items(), key=lambda x: x[1], reverse=True)

# 言葉とその頻度
word_freq = []
for word, count in keys[:20]:  # 上位何個
    word_freq.append([word, count])
    # print("{0}({1}) ".format(word, count), end="")

# データ型変換
word_freq_df = pd.DataFrame(word_freq, columns=["基本形", "頻度"])

# フレーム結合
score_df = pd.merge(word_freq_df, word_Data, on=["基本形"], how="left")

# トレンド(指数)
score_df["トレンド"] = score_df["頻度"] * score_df["スコア"]

# 言葉とそのトレンド
result_df = score_df.loc[:, ['基本形', "読み", "トレンド"]]
# トレンド降順
result_df = result_df.sort_values(by="トレンド", ascending=False)

print(result_df)

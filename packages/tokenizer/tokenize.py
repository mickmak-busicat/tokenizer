# -*- coding: utf-8 -*-
import jieba
import jieba.posseg as pseg
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import re, json

def tokenize_zh(text):
  words = jieba.lcut(text)
  return words

def get_chinese_stop_words():
  chinese_stop_words = []
  with open('./data/stop_words.json', 'r') as fp:
    chinese_stop_words = json.load(fp)

  return chinese_stop_words

def emoji_stem(text):
  very_positive = ['😍', '😂', '🤣', '🥰', '😆', '🤩', '🤪', '💕', '🤤', '🥳', '💯']
  positive = ['👍', '😋', '⭐', '✨', '🌟', '❤', '💛', '☺', '😚', '😌', '😛', '👅', '😝', '😎', '😊', '👏', '🥺', '🤗', '😳', '😉', '😙', '😁', '😜', '😻', '👌', '😜']
  negative = ['🙈', '🤭', '😅', '😢', '😥', '😒', '😕', '😔', '🙁', '☹️', '😟']
  very_negative = ['😭', '🤮', '👎', '😫', '😰', '😨', '😓', '🥵', '🤬', '😡', '😠', '😩', '😣']
  modified = text
  modified = re.sub(r"[{}]+".format(''.join(very_positive)), '😍', modified)
  modified = re.sub(r"[{}]+".format(''.join(positive)), '😊', modified)
  modified = re.sub(r"[{}]+".format(''.join(negative)), '😅', modified)
  modified = re.sub(r"[{}]+".format(''.join(very_negative)), '😭', modified)
  return modified

def is_eng_review(body):
  no_eng = re.sub(r"([a-zA-Z]+|\[IMG:[0-9]+\]|\[[a-zA-Z]+\]|\s+)", "", body)
  score = (len(no_eng)/len(body) * 100)
  return score < 10

def tokenize_body(body):
  jieba.load_userdict('./data/wordlist.txt')

  no_emote = re.sub(r"(:[a-zA-Z]+:|\\n|\\r|\n|\r|:D|:P|\[\/?[a-zA-Z]+\]|\[IMG:[0-9]+\])", "", body)
  no_emote = emoji_stem(no_emote)
  porter = PorterStemmer()

  if len(no_emote) is 0:
    return []

  token_count = token_count + 1

  if is_eng_review(no_emote):
    text = re.sub('<[^>]*>', '', no_emote)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)
    text = re.sub('[\W]+', ' ', text.lower()) + ' '.join(emoticons).replace('-', '')
    tokens = [porter.stem(word) for word in text.split()]
    stop = stopwords.words('english')
    return [w for w in tokens if w not in stop]
  else:
    punc = "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.⋯,!:()$ ></=+-~?!{}#%&*"
    no_punc = re.split(r"[{}]+".format(punc), no_emote)
    no_punc = ''.join(no_punc)
    no_punc = no_punc.replace(u'\xa0', '')

    tokens = jieba.lcut(no_punc)

    final_tokens = [token for token in tokens if re.search(r"([0-9A-Za-z]+)", token) is None]

    return final_tokens

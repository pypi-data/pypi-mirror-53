#encoding=utf-8
from __future__ import unicode_literals
import sys
sys.path.append("../")
from AutoBUlidVocabulary import Vocab

word_list=["哈士奇","狗子"]
vocab=Vocab()
vocab_list=vocab.vocab_list(word_list)
print(vocab_list)
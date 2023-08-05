[![Build Status](https://travis-ci.org/himkt/tiny_tokenizer.svg?branch=master)](https://travis-ci.org/himkt/tiny_tokenizer)
[![GitHub stars](https://img.shields.io/github/stars/himkt/tiny_tokenizer.svg?maxAge=2592000&colorB=blue)](https://github.com/himkt/tiny_tokenizer/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/himkt/tiny_tokenizer.svg)](https://github.com/himkt/tiny_tokenizer/issues)
[![GitHub release](https://img.shields.io/github/release/himkt/tiny_tokenizer.svg?maxAge=2592000&colorB=red)](https://github.com/himkt/tiny_tokenizer)
[![MIT License](http://img.shields.io/badge/license-MIT-yellow.svg?style=flat)](LICENSE)

### Overview

Tiny Tokenizer is simple sentence/word Tokenizer which is convenient to pre-process Japanese text.

<div align="center"><img src="./static/image/tiny_tokenizer.png" width="700"/></div>

### Quick Start

#### Install tiny_tokenizer on local machine

`tiny_tokenizer` uses following libraries.
- MeCab (and [natto-py](https://github.com/buruzaemon/natto-py))
- KyTea (and [Mykytea-python](https://github.com/chezou/Mykytea-python))
- Sudachi ([SudachiPy](https://github.com/WorksApplications/SudachiPy))
- Sentencepiece ([Sentencepiece](https://github.com/google/sentencepiece))

It is not needed for sentence level tokenization because these libraries are used in word level tokenization.
You can install tiny_tokenizer and above libraries by pip, please run:
`pip install tiny_tokenizer`.

Or, you can install tiny_tokenizer only with SentenceTokenizer by the following command:
`BUILD_WORD_TOKENIZER=0 pip install tiny_tokenizer`.


#### Install tiny_tokenizer on Docker container

You can use tiny_tokenizer using the Docker container.
If you want to use tiny_tokenizer with Docker, run following commands.

```
docker build -t himkt/tiny_tokenizer .
docker run -it himkt/tiny_tokenizer
```


### Example

`python3 example/tokenize_document.py`

<details>

```
# python3 example/tokenize_document.py
Finish creating word tokenizers

Given document: 我輩は猫である。名前はまだない
#0: 我輩は猫である。
Tokenizer: MeCab
[我輩, は, 猫, で, ある, 。]
Tokenizer: MeCab
[我輩 (名詞), は (助詞), 猫 (名詞), で (助動詞), ある (助動詞), 。 (記号)]
Tokenizer: KyTea
[我輩, は, 猫, で, あ, る, 。]
Tokenizer: KyTea
[我輩 (名詞), は (助詞), 猫 (名詞), で (助動詞), あ (動詞), る (語尾), 。 (補助記号)]
Tokenizer: Sentencepiece
[▁, 我, 輩, は, 猫, である, 。]
Tokenizer: Sudachi (A)
[我輩, は, 猫, で, ある, 。]
Tokenizer: Sudachi (A)
[我輩 (代名詞), は (助詞), 猫 (名詞), で (助動詞), ある (動詞), 。 (補助記号)]
Tokenizer: Sudachi (B)
[我輩, は, 猫, で, ある, 。]
Tokenizer: Sudachi (B)
[我輩 (代名詞), は (助詞), 猫 (名詞), で (助動詞), ある (動詞), 。 (補助記号)]
Tokenizer: Sudachi (C)
[我輩, は, 猫, で, ある, 。]
Tokenizer: Sudachi (C)
[我輩 (代名詞), は (助詞), 猫 (名詞), で (助動詞), ある (動詞), 。 (補助記号)]
Tokenizer: Character
[我, 輩, は, 猫, で, あ, る, 。]

#1: 名前はまだない
Tokenizer: MeCab
[名前, は, まだ, ない]
Tokenizer: MeCab
[名前 (名詞), は (助詞), まだ (副詞), ない (形容詞)]
Tokenizer: KyTea
[名前, は, まだ, な, い]
Tokenizer: KyTea
[名前 (名詞), は (助詞), まだ (副詞), な (形容詞), い (語尾)]
Tokenizer: Sentencepiece
[▁, 名前, はまだ, ない]
Tokenizer: Sudachi (A)
[名前, は, まだ, ない]
Tokenizer: Sudachi (A)
[名前 (名詞), は (助詞), まだ (副詞), ない (形容詞)]
Tokenizer: Sudachi (B)
[名前, は, まだ, ない]
Tokenizer: Sudachi (B)
[名前 (名詞), は (助詞), まだ (副詞), ない (形容詞)]
Tokenizer: Sudachi (C)
[名前, は, まだ, ない]
Tokenizer: Sudachi (C)
[名前 (名詞), は (助詞), まだ (副詞), ない (形容詞)]
Tokenizer: Character
[名, 前, は, ま, だ, な, い]
```

</details>


### Test

```
python -m pytest
```

### Acknowledgement

Sentencepiece model used in test is provided by @yoheikikuta. Thanks a lot!

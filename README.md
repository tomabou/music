# leap musician

## Desctiption
LeapMotionを用いて、簡単に曲を奏でることが出来るシステム


## Requirements

- Windows
- python 2.7 (LeapMotion apiの都合上python2.7を用います)
- pyaudio 0.2.11
- python-rtmidi 1.3.0
- LeapMotion SDK v3.2
- Midi出力を受け取るデバイス

## Setup
[LeapMotionSDK v3.2](https://developer.leapmotion.com/releases/leap-motion-orion-321)をインストールする

* [VSTHost](http://www.hermannseib.com/english/vsthost.htm)を用いて適当なVSTiを再生出来るようにする
* [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)などの仮想midiケーブルを用意する

leap_musician.py内のCHANNEL_NUM番目までのmidi channelに出力をするので、各channelに好きなシンセサイザーを対応させておく

## Usage
LeapMotionを接続する

loopMIDI VSTHostを起動する

```
python leap_musician.py
```
で実行する

Midiデバイス一覧が表示されるので、使用したいmidiデバイスのindexを入力する

両手を握りしめると曲がスタートする

手を上下に動かすと曲に合わせる音が出る

手をひっくり返すと出力Channelを切り替えることで楽器を切り替えることが出来る

曲が変わるタイミングで手を握ると、再生する曲を変更することが出来る
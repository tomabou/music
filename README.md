# music

## 概要
1. 音声をリアルタイムに出力できるようにする
2. Leap MotionのAPIを叩けるようにする
3. コード進行のサンプルを作る
4. バッキングを作成する(DTM)
5. 数個の入力により、バッキングにあった音が生成される部分を書く　このとき、テンションの概念を用いる対位法的な話も少し入れられたらいいかも知れない

上記を組み合わせれば完成である

## ライブラリ選定
音声IO: PyAudioがいいんじゃなかろうかと感じる

PyAudioを使ってバッキングの音声ファイルは出力できそう

メロディーはどうやって出力するのか
1. MIDIで外部機器
2. 直接wavを再生
3. MIDIでVSTi

MIDIのライブラリの使いやすければ1が良い気がする
MIDIデバイス周りが全然わからないのが難点（どうやって接続すれば良いのか）
RtMidiというC++ライブラリはあった
midoとかいうpythonライブラリは使いやすそう
midiメッセージを投げて終わりなので、その後audioデータを受け取らなきゃいけないVSTiに比べるとかなり楽そうである
音声出力との同期が不安だが、そこのディレイは調整すれば大丈夫そう
この方針で行ってみるか

2は力技だが、エフェクトとかリバーブとか適切にかけられるかどうかが不安

3は多分VSTiホストのライブラリが必要　C++にはありそうだが、pythonにあるんだろうか
steinbergの公開しているC++SDKがあった C#でも大丈夫そう

MIDI出力を受け取るのは実機のシンセサイザーじゃなきゃいけないのか？
仮想シンセサイザーでは無理なのか
これは音声ををミックスするみたいな処理をOSの機能に投げつけている（違うアプリケーションで同時に音を出してうまくまじり合わさることを期待している）
VSTiを使うならそれは自力で頑張るということになる
ちょっと行儀がわるいのかもしれない？正しい使い方？
実機で出せば良いのならそれはそれで良い

LeapMotionを控室で発見
windowsにSDKを入れてちゃんと動作することを確認
ubuntuで動くかあとで確認する

ubuntuでv2.3.1のapiが動くことを確認した
https://futurismo.biz/archives/6655/
このサイトにはインストールがfailすると書いてあったが、特にエラーを吐かずにインストール出来た
Visualizerは結構不安定
v2.3.1を動かして思ったがかなり不安定である
windows上で動くV4のほうがかなりトラッキングの精度が高いと感じた。Midiとの相性もあるのでwindowsで開発したほうが丸いかもしれない

windows上で環境構築するのが面倒かと一瞬思ったが、scoopという神ツールの存在を知ったので一気にやる気になった
今回はwindows上で頑張ることにする
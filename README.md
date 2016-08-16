
# suikin

集めたデータが無い状態から実行する方法

1. main/createSoundAndFFT.py を実行して録音&FFT
   これを5回行う（クラスタリングで空のクラスタができないように）。
2. clustering/test_kmeans.py を実行してクラスタリング
3. main/main.pyを実行

===================

以下メモ書き
-録音してFFTした結果をfft.pklとして
hayakuti_data/???/に保存。
それをクラスタリングした結果を
?.pklに保存。
そうすれば動く。

python writingWavAndPng.py

mainの流れ
wavname -> fs, data -> fftして


# suikin

集めたデータが無い状態から実行する方法

-録音してFFTした結果をfft.pklとして
hayakuti_data/???/に保存。
それをクラスタリングした結果を
?.pklに保存。
そうすれば動く。

python writingWavAndPng.py

mainの流れ
wavname -> fs, data -> fftして

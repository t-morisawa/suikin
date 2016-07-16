
# 音声入力関係のメソッドを置く場所

## FFT


## 雑多な情報

### 1.入力
```python
input = stream.read(CHUNK) #バイナリで取得
input = np.frombuffer(input, dtype="int16") / 32768.0 #16bitの整数型に変換
``` 

### 2.フィルタリング
```python
input = scipy.signal.lfilter(b, 1, input)　#フィルタした信号
``` 

### 3.バイナリに戻す
```python
input = [int(v * 32767.0) for v in input]
input = struct.pack("h" * len(input), *input)
``` 

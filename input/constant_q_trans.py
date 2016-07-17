# -*- coding: utf-8 -*-
"""
Efficient Constant-Q Transform (with FFT)
Moranral rcording.

Thanks:http://yukara-13.hatenablog.com/entry/2014/01/05/062414

"""
from scipy import arange, ceil, complex128, dot, exp, float64, hamming, log2, zeros
from scipy import pi as mpi
from scipy.fftpack import fft
from scipy.sparse import lil_matrix, csr_matrix
from scipy.io.wavfile import read

from matplotlib import pylab as pl

# 対数周波数ビン数を計算
def get_num_freq(fmin, fmax, fratio):
    return int(round(log2(float(fmax) / fmin) / fratio)) + 1

# 各対数周波数ビンに対応する周波数を計算
def get_freqs(fmin, nfreq, fratio):
    return fmin * (2 ** (arange(nfreq) * fratio))

two_pi_j = 2 * mpi * 1j

### default parameters
fmin_default = 60 # min of frequency
fmax_default = 6000 # max of frequency
fratio_default = 1. / 24 # fratio (24 freq bins per 1 octave)
q_rate_def = 20. * fratio_default # qrate

def cq_fft(sig, fs, q_rate = q_rate_def, fmin = fmin_default, fmax = fmax_default, 
           fratio = fratio_default, win = hamming, spThresh = 0.0054):
    # 100 frames per 1 second
    nhop = int(round(0.01 * fs))
    
    # Calculate Constant-Q Properties
    nfreq = get_num_freq(fmin, fmax, fratio) # number of freq bins
    freqs = get_freqs(fmin, nfreq, fratio) # freqs [Hz]
    Q = int((1. / ((2 ** fratio) - 1)) * q_rate) # Q value
 
    # Preparation
    L = len(sig)
    nframe = L / nhop # number of time frames

    # N  > max(N_k)
    fftLen = int(2 ** (ceil(log2(int(float(fs * Q) / freqs[0])))))
    h_fftLen = fftLen / 2
   
    # ===================
    #  カーネル行列の計算
    # ===================
    sparseKernel = zeros([nfreq, fftLen], dtype = complex128)
    for k in xrange(nfreq):
        tmpKernel = zeros(fftLen, dtype = complex128)
        freq = freqs[k]
        # N_k 
        N_k = int(float(fs * Q) / freq)
        # FFT窓の中心を解析部分に合わせる．
        startWin = (fftLen - N_k) / 2
        tmpKernel[startWin : startWin + N_k] = (hamming(N_k) / N_k) * exp(two_pi_j * Q * arange(N_k, dtype = float64) / N_k)
        # FFT (kernel matrix)
        sparseKernel[k] = fft(tmpKernel)

    ### 十分小さい値を０にする
    sparseKernel[abs(sparseKernel) <= spThresh] = 0
    
    ### スパース行列に変換する
    sparseKernel = csr_matrix(sparseKernel)
    ### 複素共役にする
    sparseKernel = sparseKernel.conjugate() / fftLen
 
    ### New signal (for Calculation)
    new_sig = zeros(len(sig) + fftLen, dtype = float64)
    new_sig[h_fftLen : -h_fftLen] = sig
    ret = zeros([nframe, nfreq], dtype = complex128)
    for iiter in xrange(nframe):
        #print iiter + 1, "/", nframe
        istart = iiter * nhop
        iend = istart + fftLen
        # FFT (input signal)
        sig_fft = fft(new_sig[istart : iend])
        # 行列積
        ret[iiter] = sig_fft * sparseKernel.T
 
    return ret, freqs

if __name__ == "__main__":
    import numpy as np
    import cv2
    wavfile = "data/2.wav" # your sample data
    fs, data = read(wavfile)
    cq_spec, freqs = cq_fft(data, fs)
    print cq_spec
    w, h = cq_spec.shape

    fig = pl.figure()
    fig.add_subplot(111)
    pl.imshow(abs(cq_spec).T, aspect = "auto", origin = "lower")
    pl.tick_params(labelbottom='off')
    pl.tick_params(labelleft='off')
    pl.savefig("hoge",bbox_inches='tight')

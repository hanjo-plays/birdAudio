# Audio processing utilities for converting raw audio into mel spectrograms for bird species classification.

import numpy as np
import librosa



SAMPLE_RATE = 32000 # In Hz. Nyquist is double the max frequency, so 32kHz allows up to 16kHz which covers most bird vocalizations.
SEGMENT_LENGTH = 3.0 # Long enough probably. In Seconds
# Raw audio (96000 samples)
#     → RMS check: is it silent? If yes, skip entirely
#     → FFT windows: slide 2048-sample window, hop 512, get frequencies at each step
#     → Mel filterbank: keep 150–15000Hz, group into 128 bins
#     → Log scale: convert to dB
#     → Output: (128, 188) numpy array
SAMPLES_PER_SEGMENT = int(SAMPLE_RATE * SEGMENT_LENGTH) # Number of samples in a 3-second segment at 32kHz for the cnn input size.
RMS_SILENCE_THRESHOLD = 0.01 # Root Mean Square of the amplitude waves. Square because the negative and positive can cancel out otherwise.

MEL_BINS = 128  # Number of frequency bins in the mel spectrogram.
                # Mel spectrogram converts 1D audio into a 2D array (128 x 188) — like an image.
                # Rows = frequency bands, columns = time steps, values = loudness.
                # Each bird species has a distinct visual pattern the CNN learns to recognise.
                # "Mel" scales frequencies to match human hearing — more detail in low frequencies
                # where bird calls vary most.
                # Kind of like the dimensions of a photo — too small and you lose detail, too large and it's harder to learn patterns. 
                # 128 is a common sweet spot for audio tasks.
                
                
# FFT is fast fourier transform, which is converting frequencies from the time domain to frequency domain.
# Think of it like this: you hear a chord on a piano. The raw audio is just one combined waveform. 
# The Fourier transform tells you "that's a C, an E, and a G being played together" — it separates the individual notes.
# Your CNN can't learn to recognise bird species from the raw wiggly line. 
# But when you convert to a spectrogram using FFT, the Great Tit shows a bright horizontal band at 4000–6000Hz, the Wood Pigeon shows a band at 300–500Hz, and the CNN can learn "bright band at this height = this species." 
# The patterns become visible and learnable.
FFT_WINDOW_SIZE  = 2048 # Window size is the number of samples in each FFT frame (64ms at 32kHz). 
                        # This is needed to divide the signals into windows for FFT
                        # Too large → frequencies blend across time, losing temporal detail.
                        # Too small → not enough wave cycles to distinguish similar frequencies.
                        
# Window 1: [========2048========]
# Window 2:      [========2048========]         ← slid forward 512 samples
# Window 3:           [========2048========]    ← slid forward another 512                        
FFT_HOP_SIZE = 512  # Samples to slide forward between FFT windows.
                    # Creates 75% overlap with 2048 window (2048 - 512 = 1536 shared).
                    # Smaller hop → more columns, smoother time detail, slower processing.
                    # Larger hop → fewer columns, risk missing short events between windows.
                    # 512 gives 188 time steps per 3s segment — good balance.
                    
MIN_FREQUENCY_HZ = 150    # Cut below 150Hz — wind, traffic, mic rumble. No birds here.
MAX_FREQUENCY_HZ = 15000  # Cut above 15kHz — insects, mic artifacts. Birds don't go this high.


def audio_to_segments(filepath):
    """Load an mp3 and split into 3-second segments, discarding silent ones."""
    try:
        y, sr = librosa.load(filepath, sr=SAMPLE_RATE, mono=True)
    except Exception as e:
        print(f"  Failed to load {filepath}: {e}")
        return []

    segments = []
    for start in range(0, len(y) - SAMPLES_PER_SEGMENT, SAMPLES_PER_SEGMENT): # Slide through the audio in 3-second chunks
        segment = y[start:start + SAMPLES_PER_SEGMENT]

        rms = np.sqrt(np.mean(segment ** 2))
        if rms < RMS_SILENCE_THRESHOLD:
            continue

        segments.append(segment)

    return segments


def segment_to_mel(segment):
    """Convert a 3-second audio segment to a mel spectrogram."""
    mel_spec = librosa.feature.melspectrogram(
        y=segment,
        sr=SAMPLE_RATE,
        n_mels=MEL_BINS,
        n_fft=FFT_WINDOW_SIZE,
        hop_length=FFT_HOP_SIZE,
        fmin=MIN_FREQUENCY_HZ,
        fmax=MAX_FREQUENCY_HZ
    )
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    return mel_spec_db
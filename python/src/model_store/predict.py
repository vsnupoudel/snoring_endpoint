from  model_load import model
from scipy.io import wavfile
from scipy.signal import resample
import tensorflow as tf

my_classes = {  0: 'Not_snoring', 
                1: 'Snoring'     }

def ensure_sample_rate(original_sample_rate, waveform,
                       desired_sample_rate=16000):
  """Resample waveform if required."""
  if original_sample_rate != desired_sample_rate:
    desired_length = int(round(float(len(waveform)) /
                               original_sample_rate * desired_sample_rate))
    waveform = resample(waveform, desired_length)
  return desired_sample_rate, waveform

def is_snoring(wav_file_name):
    sample_rate, wav_data = wavfile.read(wav_file_name, 'rb')
    sample_rate, wav_data = ensure_sample_rate(sample_rate, wav_data)
    waveform = wav_data / tf.constant( wav_data.max(), dtype=tf.float32)
    result = model(waveform).numpy()
    return bool( result.argmax() )

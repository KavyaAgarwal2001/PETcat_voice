import numpy as np
import scipy as sp
from scipy.io.wavfile import read
from scipy.io.wavfile import write     # Imported libaries such as numpy, scipy(read, write), matplotlib.pyplot
from scipy import signal
import matplotlib.pyplot as plt
import sys
import pyaudio
import wave
# get_ipython().magic('matplotlib inline')

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
# RECORD_SECONDS = 3
# In[10]:


# Replace this with the location of your downloaded file.
(Frequency, array) = read(sys.argv[1]) # Reading the sound file. 


# In[11]:


# len(array) # length of our array


# In[12]:


plt.plot(array) 
plt.title('Original Signal Spectrum')
plt.xlabel('Frequency(Hz)')
plt.ylabel('Amplitude')
plt.show()


# In[13]:


FourierTransformation = sp.fft(array) # Calculating the fourier transformation of the signal


# In[14]:


scale = sp.linspace(0, Frequency, len(array))


# In[15]:


# plt.stem(scale[0:5000], np.abs(FourierTransformation[0:5000]), 'r')  # The size of our diagram
# plt.title('Signal spectrum after FFT')
# plt.xlabel('Frequency(Hz)')
# plt.ylabel('Amplitude')
# plt.show()


# In[16]:


# GuassianNoise = np.random.rand(len(FourierTransformation)) # Adding guassian Noise to the signal.


# In[17]:


# NewSound = GuassianNoise + array


# In[18]:


# write("New-Sound-Added-With-Guassian-Noise.wav", Frequency, NewSound) # Saving it to the file.


# In[19]:


b,a = signal.butter(5, 1000/(Frequency/2), btype='highpass') # ButterWorth filter 4350


# In[20]:


filteredSignal = signal.lfilter(b,a,array)
plt.plot(filteredSignal) # plotting the signal.
plt.title('Highpass Filter')
plt.xlabel('Frequency(Hz)')
plt.ylabel('Amplitude')
plt.show()


# In[21]:


c,d = signal.butter(5, 1000/(Frequency/2), btype='lowpass') # ButterWorth low-filter
newfilteredSignal = signal.lfilter(c,d,filteredSignal) # Applying the filter to the signal
plt.plot(newfilteredSignal) # plotting the signal.
plt.title('Lowpass Filter')
plt.xlabel('Frequency(Hz)')
plt.ylabel('Amplitude')
plt.show()

newfilteredSignal =np.asarray(newfilteredSignal)
# In[22]:


# write("output.wav", Frequency, newfilteredSignal) # Saving it to the file
waveFile = wave.open("output.wav", 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(2)
waveFile.setframerate(RATE)
waveFile.writeframes(newfilteredSignal)
waveFile.close()
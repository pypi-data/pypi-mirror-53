# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 15:28:52 2019

@author: xuan
"""
import pickle

"""
-------- Specify path and file name --------
"""
path = './'
pickle_filename = '20181221_Greyson_Cage_002.pkl'
with open ( ''.join((path, pickle_filename)), 'rb' ) as fp:
    my_cage_data = pickle.load(fp)

"""
-------- Here are important attributes of the cage data structure. --------
"""
#-------- spike times --------#
spikes = my_cage_data.spikes
#-------- spike channel id --------#
spike_ch_lbl = my_cage_data.ch_lbl
#-------- spike waveforms --------#
waveforms = my_cage_data.waveforms

#-------- Muscle names --------#
EMG_names = my_cage_data.EMG_names
#-------- Raw EMG data without filtering --------#
raw_EMG = my_cage_data.EMG_diff
#-------- Filtered EMG at 2 kHz --------#
filtered_EMG = my_cage_data.filtered_EMG

"""
-------- Bin data with this function: --------
"""
bin_size = 0.01
my_cage_data.bin_data(bin_size, mode = 'center')
# Here the 'mode' parameter spcifies the way of binning.
# The default setting is 'center', meaning each bin is centered on the sampling time point
# If the mode is set to 'left', then the spike counts are calculated on the left side of the sampling time point
"""
-------- Binned data are stored in a dictionary array named "binned" --------
"""
timeframe = my_cage_data.binned['timeframe']
binned_spikes = my_cage_data.binned['spikes']
binned_filtered_EMG = my_cage_data.binned['filtered_EMG']

"""
-------- If smoothing is needed, this function can be used --------
"""
my_cage_data.smooth_binned_spikes('gaussian', 0.05)
# -------- Smoothed spikes can be obtained like this: --------#
smoothed_binned_spikes = my_cage_data.binned['spikes']
# Data smoothing is directly applied on binned spikes. So if you don't need smoothing, don't run the smooth function

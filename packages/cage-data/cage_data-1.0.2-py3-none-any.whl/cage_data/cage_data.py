# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 22:38:27 2019

@author: xuan
"""

import numpy as np
import _pickle as pickle
import time
from .brpylib import NevFile 
from .load_intan_rhd_format import read_data
from scipy import stats, signal
from .intanutil.notch_filter import notch_filter

class cage_data:
    def __init__(self):
        print('An empty cage_data object has been created.')
        
    def create(self, path, nev_file, rhd_file, empty_channels, do_notch = 0):
        """
        'nev_file' is the neural data file,
        'rhd_file' is the EMG data file
        """
        self.nev_fs = 30000
        if path[-1] == '/':
            self.nev_file = ''.join((path, nev_file))
            self.rhd_file = ''.join((path, rhd_file))
        else:
            self.nev_file = ''.join((path, '/', nev_file))
            self.rhd_file = ''.join((path, '/', rhd_file))
        self.spikes, self.waveforms, self.ch_lbl = self.parse_nev_file(self.nev_file, empty_channels)
        try:
            self.date_num = int(rhd_file[:8])
            self.date_num = 0
        except ValueError:
            print('Check the file name of the .rhd file!')
        else:
            pass
        self.EMG_names, self.EMG_diff, self.EMG_timeframe = self.parse_rhd_file(self.rhd_file, do_notch)
        self.file_length = self.EMG_timeframe[-1]
        print(self.EMG_names)
        self.is_cortical_cleaned = False
        self.is_EMG_filtered = False
        self.pre_processing_summary()
        
    def pre_processing_summary(self):
        print('EMG filtered? -- %s' %(self.is_EMG_filtered))
        print('Cortical data cleaned? -- %s' %(self.is_cortical_cleaned))
    
    def parse_nev_file(self, filename, empty_channels):
        empty_str = []
        for each in empty_channels:
            empty_str.append(''.join(('elec', str(each))))
        chans = list(np.arange(1, 97, 1))
        s = time.clock()
        nev_file = NevFile(filename)
        self.basic_header = nev_file.basic_header
        self.extended_header = nev_file.extended_headers
        ch_lbl = []
        for i in range(len(chans)):
            lbl_idx = next(idx for (idx, d) in enumerate(nev_file.extended_headers)
                           if d['PacketID'] == 'NEUEVLBL' and d['ElectrodeID'] == chans[i])
            lbl = nev_file.extended_headers[lbl_idx]['Label']
            ch_lbl.append(lbl)
        bad_num = []
        for each in empty_str:
            bad_num.append(ch_lbl.index(each))
        del_chans, del_lbls = [], []
        for each in bad_num:
            del_chans.append(chans[each])
            del_lbls.append(ch_lbl[each])
        for i in range(len(bad_num)):
            idx = ch_lbl.index(del_lbls[i])
            del(ch_lbl[idx])
            idx = chans.index(del_chans[i])
            del(chans[idx])
        nev_data = nev_file.getdata(chans)
        spike_events = nev_data['spike_events']
        nev_file.close()
        e = time.clock()
        print(e-s)
        spikes = spike_events['TimeStamps']
        for i in range(len(spikes)):
            spikes[i] = np.asarray(spikes[i])
        waveforms = spike_events['Waveforms']
        ch_id = spike_events['ChannelID']
        self.ch_id = ch_id
        s_spikes = []
        s_waveforms = []
        for each in chans:
            idx = ch_id.index(each)
            s_spikes.append(spikes[idx])
            s_waveforms.append(waveforms[idx])
        return s_spikes, s_waveforms, ch_lbl
        
    def parse_rhd_file(self, filename, notch):
        rhd_data = read_data(filename)
        if self.date_num < 20190701:
            self.EMG_fs = 2011.148
        else:
            self.EMG_fs = rhd_data['frequency_parameters']['amplifier_sample_rate']
        EMG_single = rhd_data['amplifier_data']
        if notch == 1:
           for i in range(np.size(EMG_single, 0)): 
               EMG_single[i,:] = notch_filter(EMG_single[i,:], self.EMG_fs, 60, 10)
        else:
            pass
        EMG_names_single = []
        for i in range(len(rhd_data['amplifier_channels'])):
            EMG_names_single.append(rhd_data['amplifier_channels'][i]['custom_channel_name'])
        EMG_names = []
        EMG_index1 = []
        EMG_index2 = []
        for i in range(len(EMG_names_single)):
            temp_str = EMG_names_single[i][:-2]
            if (temp_str in EMG_names) == True:
                continue
            else:
                for j in range(i+1, len(EMG_names_single)):
                    temp_str2 = EMG_names_single[j]
                    if temp_str2.find(temp_str) != -1:
                        EMG_names.append(temp_str)
                        EMG_index1.append(EMG_names_single.index(EMG_names_single[i]))
                        EMG_index2.append(EMG_names_single.index(EMG_names_single[j]))
        EMG_diff = []
        for i in range(len(EMG_index1)):
            EMG_diff.append(EMG_single[EMG_index1[i], :] - EMG_single[EMG_index2[i], :])
        EMG_diff = np.asarray(EMG_diff)
        sync_line0 = rhd_data['board_dig_in_data'][0]
        sync_line1 = rhd_data['board_dig_in_data'][1]
        d0 = np.where(sync_line0 == True)[0]
        d1 = np.where(sync_line1 == True)[0]
        ds = int(d1[0] - int((d1[0]-d0[0])*0.2))
        de = int(d1[-1] + int((d0[-1]-d1[-1])*0.2))
        rhd_timeframe = np.arange(de-ds+1)/self.EMG_fs
        return EMG_names, list(EMG_diff[:, ds:de]), rhd_timeframe
    
    def clean_cortical_data(self):
        for i in range(len(self.waveforms)):
            bad_waveform_ind = []
            for j in range(np.size(self.waveforms[i], 0)):
                if (max(self.waveforms[i][j,:]) >= 400000) | (min(self.waveforms[i][j,:]) <= -400000):
                    bad_waveform_ind.append(j)
                if self.waveforms[i][j, 0] >= 95000:
                    bad_waveform_ind.append(j)
            self.waveforms[i] = np.delete(self.waveforms[i], bad_waveform_ind, axis = 0)
            self.spikes[i] = np.delete(self.spikes[i], bad_waveform_ind)
            self.is_cortical_cleaned = True

    def EMG_filtering(self, f_Hz):
        fs = self.EMG_fs
        raw_EMG_data = self.EMG_diff
        filtered_EMG = []    
        bhigh, ahigh = signal.butter(4,50/(fs/2), 'high')
        blow, alow = signal.butter(4,f_Hz/(fs/2), 'low')
        for each in raw_EMG_data:
            temp = signal.filtfilt(bhigh, ahigh, each)
            f_abs_emg = signal.filtfilt(blow ,alow, np.abs(temp))
            filtered_EMG.append(f_abs_emg)   
        self.filtered_EMG = filtered_EMG
        print('All EMG channels have been filtered.')
        self.is_EMG_filtered = True
            
    def bin_spikes(self, bin_size, mode = 'center'):
        print('Binning spikes with %.4f s' % (bin_size))
        binned_spikes = []
        if mode == 'center':
            bins = np.arange(bin_size - bin_size/2, 
                             self.EMG_timeframe[-1] + bin_size/2, bin_size)
        elif mode == 'left':
            bins = np.arange(self.EMG_timeframe[0], self.EMG_timeframe[-1], bin_size)
        bins = bins.reshape((len(bins),))
        for each in self.spikes:
            each = each/self.nev_fs
            each = each.reshape((len(each),))
            out, _ = np.histogram(each, bins)
            binned_spikes.append(out)
        bins = np.arange(self.EMG_timeframe[0], self.EMG_timeframe[-1], bin_size)
        return bins[1:], binned_spikes        
      
    def EMG_downsample(self, new_fs):
        if hasattr(self, 'filtered_EMG'):
            down_sampled = []
            n = self.EMG_fs/new_fs
            length = int(np.floor(np.size(self.filtered_EMG[0])/n)+1)
            for each in self.filtered_EMG:
                temp = []
                for i in range( 1, length ):
                    temp.append(each[int(np.floor(i*n))])
                temp = np.asarray(temp)
                down_sampled.append(temp)
            print('Filtered EMGs have been downsampled')
            return down_sampled
        else:
            print('Filter EMG first!')
            return 0
        
    def bin_data(self, bin_size, mode = 'center'):
        self.binned = {}
        self.binned['timeframe'], self.binned['spikes'] = self.bin_spikes(bin_size, mode)
        self.binned['filtered_EMG'] = self.EMG_downsample(1/bin_size)
        truncated_len = min(len(self.binned['filtered_EMG'][0]), len(self.binned['spikes'][0]))
        for (i, each) in enumerate(self.binned['spikes']):
            self.binned['spikes'][i] = each[:truncated_len]
        for (i, each) in enumerate(self.binned['filtered_EMG']):
            self.binned['filtered_EMG'][i] = each[:truncated_len]
        self.binned['timeframe'] = self.binned['timeframe'][:truncated_len]
        print('Data have been binned.')
    
    def smooth_binned_spikes(self, kernel_type, kernel_SD, sqrt = 0):
        smoothed = []
        if hasattr(self, 'binned'):
            if sqrt == 1:
               for (i, each) in enumerate(self.binned['spikes']):
                   self.binned['spikes'][i] = np.sqrt(each)
            bin_size = self.binned['timeframe'][1] - self.binned['timeframe'][0]
            kernel_hl = np.ceil( 3 * kernel_SD / bin_size )
            normalDistribution = stats.norm(0, kernel_SD)
            x = np.arange(-kernel_hl*bin_size, (kernel_hl+1)*bin_size, bin_size)
            kernel = normalDistribution.pdf(x)
            if kernel_type == 'gaussian':
                pass
            elif kernel_type == 'half_gaussian':
               for i in range(0, int(kernel_hl)):
                    kernel[i] = 0
            n_sample = np.size(self.binned['spikes'][0])
            nm = np.convolve(kernel, np.ones((n_sample))).T[int(kernel_hl):n_sample + int(kernel_hl)] 
            for each in self.binned['spikes']:
                temp1 = np.convolve(kernel,each)
                temp2 = temp1[int(kernel_hl):n_sample + int(kernel_hl)]/nm
                smoothed.append(temp2)
            print('The binned spikes have been smoothed.')
            self.binned['spikes'] = smoothed
        else:
            print('Bin spikes first!')
            
    def save_to_pickle(self, filename):
        with open (filename, 'wb') as fp:
            pickle.dump(self, fp)
        print('Save to %s successfully' %(filename))
        










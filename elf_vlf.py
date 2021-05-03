#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: ELF_VLF
# Author: bba4ae61d4b6de3af7e244f6994dddc70c7887f16f722797a6543e69bf73d7ec0a3b85886e2c86321b6d88fbc2b44bad3396353face31fd87e878a3f7946fbd5
# Description: Kuramoto synchronization
# Generated: Mon May  3 13:36:25 2021
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import numpy as np
import osmosdr
import sip
import sys
import time


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "ELF_VLF")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("ELF_VLF")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.offset = offset = -7230 + 0
        self.carrier_recv = carrier_recv = 100 * 1000000
        self.shiftoff = shiftoff = 700000 + offset
        self.samp_rate_rx = samp_rate_rx = 2000000
        self.samp_rate_audio = samp_rate_audio = 200000
        self.db_gain_recv = db_gain_recv = 1
        self.carrier = carrier = carrier_recv

        ##################################################
        # Blocks
        ##################################################
        self._db_gain_recv_range = Range(0, 17, 1, 1, 200)
        self._db_gain_recv_win = RangeWidget(self._db_gain_recv_range, self.set_db_gain_recv, "db_gain_recv", "counter_slider", float)
        self.top_grid_layout.addWidget(self._db_gain_recv_win, 1,1)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=samp_rate_rx // samp_rate_audio,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_freq_sink_x_1_1 = qtgui.freq_sink_f(
        	8192, #size
        	firdes.WIN_HAMMING, #wintype
        	0, #fc
        	samp_rate_audio, #bw
        	"", #name
        	2 #number of inputs
        )
        self.qtgui_freq_sink_x_1_1.set_update_time(0.01)
        self.qtgui_freq_sink_x_1_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1_1.enable_grid(True)
        self.qtgui_freq_sink_x_1_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1_1.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_1_1.disable_legend()
        
        if "float" == "float" or "float" == "msg_float":
          self.qtgui_freq_sink_x_1_1.set_plot_pos_half(not False)
        
        labels = ['Raw (dec)', 'AM demod (dec)', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["dark green", "dark blue", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [0.5, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_1_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_1_1_win)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
        	8192, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate_rx, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.1)
        self.qtgui_freq_sink_x_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_1.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_1.set_plot_pos_half(not True)
        
        labels = ['Raw', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["black", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_1_win)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_source_0.set_sample_rate(samp_rate_rx)
        self.osmosdr_source_0.set_center_freq(carrier_recv - shiftoff + offset, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(db_gain_recv, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self._carrier_range = Range(25 * 1000000, 1700 * 1000000, 1000, carrier_recv, 200)
        self._carrier_win = RangeWidget(self._carrier_range, self.set_carrier, "carrier", "counter_slider", float)
        self.top_grid_layout.addWidget(self._carrier_win, 1,2)
        self.blocks_wavfile_sink_0_0 = blocks.wavfile_sink('test_am.wav', 1, samp_rate_audio, 16)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink('test.wav', 2, samp_rate_audio, 16)
        self.blocks_rotator_cc_0_0 = blocks.rotator_cc(-2*np.pi*shiftoff/(samp_rate_rx))
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.analog_am_demod_cf_0 = analog.am_demod_cf(
        	channel_rate=samp_rate_audio,
        	audio_decim=1,
        	audio_pass=samp_rate_audio / 2 - samp_rate_audio / 10,
        	audio_stop=samp_rate_audio / 2 - samp_rate_audio / 20,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_am_demod_cf_0, 0), (self.blocks_wavfile_sink_0_0, 0))    
        self.connect((self.analog_am_demod_cf_0, 0), (self.qtgui_freq_sink_x_1_1, 1))    
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_freq_sink_x_1_1, 0))    
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_add_xx_0, 1))    
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_wavfile_sink_0, 1))    
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_wavfile_sink_0, 0))    
        self.connect((self.blocks_rotator_cc_0_0, 0), (self.qtgui_freq_sink_x_1, 0))    
        self.connect((self.blocks_rotator_cc_0_0, 0), (self.rational_resampler_xxx_0_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.blocks_rotator_cc_0_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.analog_am_demod_cf_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.blocks_complex_to_float_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.set_shiftoff(700000 + self.offset)
        self.osmosdr_source_0.set_center_freq(self.carrier_recv - self.shiftoff + self.offset, 0)

    def get_carrier_recv(self):
        return self.carrier_recv

    def set_carrier_recv(self, carrier_recv):
        self.carrier_recv = carrier_recv
        self.osmosdr_source_0.set_center_freq(self.carrier_recv - self.shiftoff + self.offset, 0)
        self.set_carrier(self.carrier_recv)

    def get_shiftoff(self):
        return self.shiftoff

    def set_shiftoff(self, shiftoff):
        self.shiftoff = shiftoff
        self.osmosdr_source_0.set_center_freq(self.carrier_recv - self.shiftoff + self.offset, 0)
        self.blocks_rotator_cc_0_0.set_phase_inc(-2*np.pi*self.shiftoff/(self.samp_rate_rx))

    def get_samp_rate_rx(self):
        return self.samp_rate_rx

    def set_samp_rate_rx(self, samp_rate_rx):
        self.samp_rate_rx = samp_rate_rx
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.samp_rate_rx)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate_rx)
        self.blocks_rotator_cc_0_0.set_phase_inc(-2*np.pi*self.shiftoff/(self.samp_rate_rx))

    def get_samp_rate_audio(self):
        return self.samp_rate_audio

    def set_samp_rate_audio(self, samp_rate_audio):
        self.samp_rate_audio = samp_rate_audio
        self.qtgui_freq_sink_x_1_1.set_frequency_range(0, self.samp_rate_audio)

    def get_db_gain_recv(self):
        return self.db_gain_recv

    def set_db_gain_recv(self, db_gain_recv):
        self.db_gain_recv = db_gain_recv
        self.osmosdr_source_0.set_gain(self.db_gain_recv, 0)

    def get_carrier(self):
        return self.carrier

    def set_carrier(self, carrier):
        self.carrier = carrier


def main(top_block_cls=top_block, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()

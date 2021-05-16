#!/usr/bin/env python3

import time, socket
import numpy as np
import matplotlib.pyplot as p
from argparse import ArgumentParser, RawTextHelpFormatter
from os import makedirs
from os.path import join, basename, exists
from numba import njit
from struct import pack, unpack
from sys import argv, stdout, exit
from math import radians
from scipy import signal
from scipy.io.wavfile import write, read


def plot_xlist(lst_y, lst_x=[], labels=[], colors=[], scatters=[], linestyles=[], title="", savepath="last_plot.png", show=0, xlabel="x", ylabel="y", chunk_size=0, shift=0, figsize=(12, 8), div_line=0, xticks=[], xticksfreq=1, projection=None, x_k=0, y_k=0, peak=0):
    fig = p.figure(1, figsize=figsize)
    #fig, ax = plt.subplots()
    axes = p.axes(projection=projection)

    if projection == "polar":
        axes.set_rmax(1)
        axes.set_rlabel_position(0)
        axes.grid(True)
        xlabel = ""
        ylabel = ""
        title += "\n"
    else:
        axes.ticklabel_format(style="plain")

    p.title(title)
    p.xlabel(xlabel)
    p.ylabel(ylabel)

    if lst_x == []:
        x = np.arange(lst_y[0].shape[0])
        if shift != 0:
            x = x + shift
        if chunk_size != 0:
            x = x * chunk_size
        for i in range(len(lst_y)):
            lst_x.append(x)
    if xticks:
        p.xticks(lst_x[0][::xticksfreq], xticks[::xticksfreq], rotation=45, fontsize=10)

    for i in range(len(lst_y)):
        if type(peak) == type(list()):
            if i in peak:
                axes_peaks(lst_y[i], axes, x=lst_x[i], x_k=x_k, y_k=y_k, chunk_size=chunk_size, shift=shift)
        elif peak:
            axes_peaks(lst_y[i], axes, x=lst_x[i], x_k=x_k, y_k=y_k, chunk_size=chunk_size, shift=shift)
        if labels == []:
            label = str(i)
        else:
            label = labels[i]
        if linestyles == []:
            linestyle = "-"
        else:
            linestyle = linestyles[i]
        if scatters == []:
            scatter = 0
        else:
            scatter = scatters[i]
        if div_line > 0:
            if type(lst_x[i]) == type(list()):
                lst_x_length = len(lst_x[i])
            else:
                lst_x_length = lst_x[i].shape[0]
            for j in range(lst_x_length):
                if lst_x[i][j] % div_line == 0:
                    p.axvline(x=lst_x[i][j], color='k', linestyle='--')
        if scatter > 0:
            if colors:
                p.scatter(lst_x[i], lst_y[i], s=scatter, label = label, linestyle=linestyle, color = colors[i])
            else:
                p.scatter(lst_x[i], lst_y[i], s=scatter, label = label, linestyle=linestyle)
        else:
            if colors:
                p.plot(lst_x[i], lst_y[i], label = label, linestyle=linestyle, color = colors[i])
            else:
                p.plot(lst_x[i], lst_y[i], label = label, linestyle=linestyle)

    p.legend()
    p.savefig(savepath)
    if show:
        p.show()
    p.close()

def plot_xspectrum(lst_y, lst_x, samp_rate, power_offset=0.000000001, complex_flag=0, db_flag=1, labels=[], colors=[], linestyles=[], title="", savepath="last_plot.png", show=0, xlabel="x", ylabel="y", chunk_size=0, shift=0, figsize=(12, 8), div_line=0, xticks=[], xticksfreq=1, zero_line=1, peak=0):
    fig = p.figure(1, figsize=figsize)
    axes = p.axes()
    axes.ticklabel_format(style="plain")

    p.title(title)
    p.xlabel(xlabel)
    p.ylabel(ylabel)

    if zero_line == 1:
        p.axvline(x=0, color='k', linestyle='--')

    power_offset = power_offset

    if xticks:
        p.xticks(lst_x[0][::xticksfreq], xticks[::xticksfreq], rotation=45, fontsize=10)

    for i in range(len(lst_y)):
        lst_y[i] = np.fft.rfft(lst_y[i])

        if   complex_flag > 0:
            lst_y[i] = np.abs(lst_y[i].real)
            lst_x[i] = np.linspace(0, samp_rate/2, lst_y[i].size)
        elif complex_flag < 0:
            lst_y[i] = np.abs(lst_y[i].imag)
            lst_x[i] = np.linspace(0, samp_rate/2, lst_y[i].size)
        else:
            lst_y[i] = np.abs(np.hstack([np.abs(lst_y[i].imag[::-1]), lst_y[i].real]))
            lst_x[i] = np.linspace(-1*samp_rate/2, samp_rate/2, lst_y[i].size)

        if db_flag:
            lst_y[i] = 10 * np.log10(lst_y[i] + power_offset)

        if type(peak) == type(list()):
            if i in peak:
                axes_peaks(lst_y[i], axes, x=lst_x[i], chunk_size=chunk_size, shift=shift)
        elif peak:
            axes_peaks(lst_y[i], axes, x=lst_x[i], chunk_size=chunk_size, shift=shift)
        if labels == []:
            label = str(i)
        else:
            label = labels[i]
        if linestyles == []:
            linestyle = "-"
        else:
            linestyle = linestyles[i]
        if div_line > 0:
            if type(lst_x[i]) == type(list()):
                lst_x_length = len(lst_x[i])
            else:
                lst_x_length = lst_x[i].shape[0]
            for j in range(lst_x_length):
                if lst_x[i][j] % div_line == 0:
                    p.axvline(x=lst_x[i][j], color='k', linestyle='--')
        else:
            if colors:
                p.plot(lst_x[i], lst_y[i], label = label, linestyle=linestyle, color = colors[i])
            else:
                p.plot(lst_x[i], lst_y[i], label = label, linestyle=linestyle)

    p.legend()
    p.savefig(savepath)
    if show:
        p.show()
    p.cla()
    p.clf()
    p.close()


def plot_spectrum(lst_y, samp_rate, title="", xlabel="x", ylabel="y", savepath="last_plot.png", figsize=(17, 8), chunk_size=0, shift=0, maximum=0, peak=0, rev_flag=0, show=0):
    fig = p.figure(1, figsize=figsize)
    axes = p.axes()
    axes.ticklabel_format(style="plain")

    p.title(title)
    p.xlabel(xlabel)
    p.ylabel(ylabel)

    for i in range(len(lst_y)):
        fft_data = np.abs(np.fft.rfft(lst_y[i]))
        xt = np.linspace(0, samp_rate/2, fft_data.size)

        if rev_flag == 0:
            samp_rate = 0
        if type(peak) == type(list()):
            if i in peak:
                axes_peaks(fft_data, axes, x=xt, chunk_size=chunk_size, shift=shift, samp_rate=samp_rate)
        elif peak:
            axes_peaks(fft_data, axes, x=xt, chunk_size=chunk_size, shift=shift, samp_rate=samp_rate)

        if maximum:
            acc = 0
            for j in range(xt.shape[0]):
                #print(j)
                if xt[j] >= maximum:
                    break
                acc += 1
            xt = xt[:acc]
            fft_data = fft_data[:acc]
        print(xt.shape[0])
        p.plot(xt, fft_data)

    #p.legend()
    p.savefig(savepath)
    if show:
        p.show()
    p.cla()
    p.clf()
    p.close()

def interval_create(carrier_freq, pulse_freqs, samp_rate, count, times, gaussian=0, noise=0, flag=1, mode="float"):
    #print(samp_rate)
    #pulse_freq = round(np.average(pulse_freqs))

    #array = np.array([], dtype="float")

    size = 0

    for i in range(pulse_freqs.shape[0]):
        duration = count * round(samp_rate / carrier_freq)
        space = round(samp_rate / pulse_freqs[i]) - duration
        size += duration + space

    array = np.zeros(size, dtype="float")

    acc = 0

    for i in range(pulse_freqs.shape[0]):
        duration = count * round(samp_rate / carrier_freq)
        space = round(samp_rate / pulse_freqs[i]) - duration
        time = np.arange(0, duration/samp_rate, 1/samp_rate)

        if gaussian == 0:
            array[acc:acc+duration] = np.sin(2*np.pi*carrier_freq * time)
        elif gaussian == -1:
            array[acc:acc+duration] = (np.sin(2*np.pi*carrier_freq * time - np.pi/2) + 1) / 2
        elif gaussian == -2:
            array[acc:acc+duration] = np.random.normal(0, 1, duration)
            array[acc:acc+duration] = array[acc:acc+duration] / np.max(array[acc:acc+duration])
        else:
            #array[acc:acc+duration] = (np.sin(2*np.pi*carrier_freq * time - np.pi/2) + 1) / 2
            for j in range(count):
                sample = duration // count
                array[acc+j*sample:acc+(j+1)*sample] = signal.gaussian(sample, std=gaussian)
        #print(pulse.shape[0])

        #array[acc:acc+duration] = pulse
        acc += duration + space

    total = np.array([])
    for i in range(times):
        total = np.hstack((total, array))

    if noise:
        total += np.random.normal(0, noise/100, total.shape[0])
        total = total / np.max(total)

    if mode == "int16":
        total = np.int16(32767 * total)

    time = np.arange(0, total.shape[0], 1) / samp_rate
    return total, time


def interval_coding(carrier_freq, interval_freqs, samp_rate, count=1, times=1, gaussian=0, noise=0, mode="int16", wav=0, show=0):
    interval_freqs = np.array(interval_freqs)
    pulse_freq = round(np.average(interval_freqs))

    array, time = interval_create(carrier_freq, interval_freqs, samp_rate, count, times, gaussian=gaussian, noise=noise, mode=mode)

    directory = "output"

    if wav:
        makedirs(directory, exist_ok=True)
        name = "pulse{:d}_carrier{:d}_count{:d}_times{:d}_g{:d}".format(pulse_freq, carrier_freq, count, times, gaussian)
        wav_path = join(directory, name+".wav")
        write(wav_path, samp_rate, array)

    if show:
        makedirs(directory, exist_ok=True)
        title = "samp_rate={:d}\npulse_freq={:.2f}, carrier_freq={:.2f}, count={:d}, times={:d}, g={:d}".format(samp_rate, pulse_freq, carrier_freq, count, times, gaussian)

        lst_y = [array]
        lst_x = [time]

        labels = ["pulse", "sine"]
        colors = ["green", "magenta"]
        linestyles = ["-", ":"]

        img_path_wave = join(directory, name+"_waveform.png")

        lst_y = [array[0:samp_rate]]   #[array]
        lst_x = [time[0:samp_rate]]    #[time]
        projection = None

        plot_xlist(lst_y, lst_x=lst_x, labels=labels, colors=colors, linestyles=linestyles, title=title, div_line=1, xticksfreq=1, xlabel="time (sec)", ylabel="amplitude", projection=projection, savepath=img_path_wave, show=show)

        #plot_xspectrum(lst_y, lst_x, samp_rate, show=show)

        #plot_spectrum(lst_y, samp_rate, show=show)

    return array



version = "0.0.6"


if __name__ == "__main__":
    banner = '''\033[1;m\033[10;32m
interval_coding                 
\033[1;m'''


    """
./interval_coding.py double.bin -f 501 -s 80000 -c 32 -t 1
./interval_coding.py double.bin -f 520 -s 80000 -c 20 -t 1
./interval_coding.py double.bin -f 2000 -s 80000 -c 20 -t 1
./interval_coding.py double.bin -f 3000 -s 80000 -c 20 -t 1
    """

    """
./interval_coding.py byte.bin -f 501 -s 80000 -c 4 -t 1 -r byte
    """

    """
./interval_coding.py "9" -f 45 -s 80000 -c 1 -t 80 -g 20
    """

    """
./interval_coding.py "7.83" -f 63 -s 44100 -c 4 -t 512
./interval_coding.py "7.83" -f 940 -s 44100 -c 8 -t 512
./interval_coding.py "7.83" -f 4009 -s 44100 -c 63 -t 512
    """

    """
./interval_coding.py "7.83" -f 501 -s 44100 -c 3 -t 300 -n 5
./interval_coding.py "7.83" -f 500 -s 44100 -c 14 -t 300 -g -2
    """

    usage = './interval_coding.py "7.83" -f 60 -s 44100 -c 4 -t 512'

    parser = ArgumentParser(description=banner,
                            formatter_class=RawTextHelpFormatter,
                            epilog=usage)

    parser.add_argument('filepath', type=str, help="Binary Data Filepath")

    parser.add_argument("-s",'--sample_rate','--rate', dest='samp_rate', type=int, default=44000, help="Sample Rate")
    parser.add_argument("-f",'--carrier', dest='carrier_freq', type=int, default=2000, help="Carrier Frequency")

    parser.add_argument("-t",'--times', dest='times', type=int, default=1, help="Repeating times")
    parser.add_argument("-c",'--count', dest='count', type=int, default=1, help="Count")

    parser.add_argument("-r",'--read', dest='read', type=str, default='double', help="[double, float, byte]")
    parser.add_argument("-m",'--mode', dest='mode', type=str, default='int16', help="Mode [int16]")

    parser.add_argument("-g",'--gaussian', dest='gaussian', type=int, default=-1, help="$\sigma$=100")
    parser.add_argument("-n",'--noise', dest='noise', type=int, default=0, help="Noise level [0 to 100]")
    
    args = parser.parse_args()

    # help/exit section
    if len(argv) == 1:
        parser.print_help()
        exit(1)

    if args.gaussian > 0:
        value = args.samp_rate / args.carrier_freq / args.gaussian
        if value < 8:
            print("[!] bad resolution: please, increase frequency (-f), increase sample_rate (-s) or decrease sigma (-g)")
            exit()

    if exists(args.filepath):
        with open(args.filepath, "rb") as f:
            print("[*] data reading...")
            if args.read in ["double", "float"]:
                if args.read == "double":
                    k = 8
                    s = "d"
                elif args.read == "float":
                    k = 4
                    s = "f"
                data = f.read()
                interval_freqs = []
                for i in range(len(data) // k):
                    chunk = data[i*k:(i+1)*k]
                    interval_freqs.append(unpack(s, chunk)[0])
                print(interval_freqs)
            else:
                interval_freqs = list(bytearray(f.read()))
            print("[*] intervals = {:d}".format(len(interval_freqs)))
            print("[*] done!")
    else:
        print("[*] data reading...")
        lst = args.filepath.split()
        interval_freqs = []
        for f in lst:
            interval_freqs.append(float(f))
        print(interval_freqs)
        print("[*] intervals = {:d}".format(len(interval_freqs)))
        print("[*] done!")

    print("[*] generating...")
    interval_coding(args.carrier_freq, interval_freqs, args.samp_rate, count=args.count, times=args.times, gaussian=args.gaussian, noise=args.noise, mode=args.mode, wav=1, show=1)
    print("[*] done!")









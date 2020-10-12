import itertools

import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

# using plotly to build plot
from matplotlib import ticker
from matplotlib.ticker import FormatStrFormatter


def build_plotly(aList, graph_name="Untitled"):
    fig = go.Figure(data=go.Scatter(y=aList, name=graph_name, line=dict(color='red', width=2)))
    fig.update_layout(title=graph_name)
    fig.write_html(graph_name + '.html', auto_open=True)


# using matplotlib to build plot
def build_plot(aList, graph_name=""):
    if (len(aList) > 300):
        plt.figure(figsize=(20, 10))


    plt.plot(aList, color='red', linewidth=1, marker='o', markersize=1)
    csfont = {'fontname': 'Times New Roman',
                          'weight': 'normal',
                            'size': 10}
    plt.title(graph_name, **csfont)
    plt.grid()
    plt.show()

def build_BER(snrindB_range,ber):
    plt.plot(snrindB_range, ber, 'o-', label='practical')
    plt.yscale('log')
    # plt.axis([0, 10, 0, 0.1])
    plt.xlabel('snr(dB)')
    plt.ylabel('BER')
    plt.grid(True)
    plt.title('BPSK Modulation')
    plt.legend()
    plt.show()

def build_BER_compare(snridB_range, *args):
    fig, ax = plt.subplots()
    marker = itertools.cycle((',', '+', '.', 'o', '*'))
    i=0
    for set in args:
        # plt.plot(snridB_range, set,label='Set '+str(i))
        ax.plot(snridB_range, set,marker=next(marker),label='Set '+str(i))
        i+=1

    plt.xlabel('snr(dB)')
    plt.ylabel('BER')
    plt.grid(True)
    plt.title('BPSK Modulation')
    plt.legend()
    ax.set_yscale('log')
    ax.set_ylim( ymax=1)
    # ax.yaxis.set_major_formatter(FormatStrFormatter('%.03f'))


    plt.show()

def build_spectrum(frequency,power_spectrum,graph_name=""):
    if (len(frequency) > 200):
        plt.figure(figsize=(20, 10))

    if (len(frequency) > 1000):
        plt.figure(figsize=(30, 10))

    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Spectrum')

    plt.plot(frequency, abs(power_spectrum),linewidth=1)
    csfont = {'fontname': 'Times New Roman',
              'weight': 'normal',
              'size': 10}
    plt.title(graph_name, **csfont)
    plt.grid()
    plt.show()

    # fig = plt.figure()
    # ax1 = fig.add_subplot(121)
    # ax2 = fig.add_subplot(122)
    # ax1.plot(frequency, abs(power_spectrum))
    # ax2.plot(frequency, abs(power_spectrum))
    #
    # scale_y = 1e2
    # ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / scale_y))
    # ax2.yaxis.set_major_formatter(ticks_y)


    # plt.stem(frequency, abs(power_spectrum),use_line_collection=True)
    # plt.show()


def build_spectrum_plotly(frequency,power_spectrum,graph_name="Untitled"):

    fig = go.Figure(data=go.Scatter(x=frequency,y=abs(power_spectrum), name=graph_name, line=dict(color='red', width=2)))
    fig.update_layout(title=graph_name)
    fig.write_html(graph_name + '.html', auto_open=True)

if __name__ == "__main__":
    a = [0,1,2,3,4,5,6,7,8,9,10]
    b = [0.3328, 0.3584, 0.256, 0.128, 0.0768, 0.0768, 0.0256, 0.0, 0.0, 0.0, 0.0]
    c = [0.2816, 0.2304, 0.1792, 0.1792, 0.0512, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    build_BER_compare(a,b,c)
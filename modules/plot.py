import matplotlib.pyplot as plt
import plotly.graph_objects as go


# using plotly to build plot
from matplotlib import ticker


def build_plotly(aList, graph_name="Untitled"):
    fig = go.Figure(data=go.Scatter(y=aList, name=graph_name, line=dict(color='red', width=2)))
    fig.update_layout(title=graph_name)
    fig.write_html(graph_name + '.html', auto_open=True)


# using matplotlib to build plot
def build_plot(aList, graph_name=""):
    plt.plot(aList, color='red', linewidth=1, marker='o', markersize=1)
    csfont = {'fontname': 'Times New Roman',
                          'weight': 'normal',
                            'size': 10}
    plt.title(graph_name, **csfont)
    plt.grid()
    plt.show()

def build_spectrum(frequency,power_spectrum):


    plt.grid()
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Spectrum')

    plt.plot(frequency, abs(power_spectrum))
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
    a = [1, 2, 3, 4]
    b = [2, 3, 4, 1]

    build_spectrum_plotly(a,b)

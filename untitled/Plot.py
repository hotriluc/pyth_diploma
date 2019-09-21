import  matplotlib.pyplot as plt
import plotly.graph_objects as go

#using plotly to build plot
def build_plotly(aList,graph_name="Untitled"):
    fig = go.Figure(data = go.Scatter( y = aList, name = graph_name,line = dict(color = 'red', width =2)))
    fig.write_html(graph_name+'.html', auto_open=True)

#using matplotlib to build plot
def build_plot(aList,graph_name):

    plt.plot(aList,color = 'red',linewidth = 1,marker ='o', markersize= 3)
    plt.suptitle(graph_name)
    plt.grid()
    plt.show()


if __name__=="__main__":
    a = [1,2,3,4]
    b = [2,3,4,1]

    build_plot(a,"kek")
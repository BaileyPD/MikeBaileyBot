import matplotlib.pyplot as plt


def basic_plot(x_data: [], y_data: [], x_title: str, y_title: str) -> plt:
    plt.plot(x_data, y_data)
    plt.ylabel(y_title)
    plt.xlabel(x_title)
    return plt


def save_plot(plot_to_save: plt, filename: str):
    plot_to_save.savefig(filename)


def show_plot(plot_to_show: plt):
    plot_to_show.show()


def create_plot_figure(x_data: [], y_data: [], x_title: str, y_title: str, filename: str):
    save_plot(basic_plot(x_data, y_data, x_title, y_title),filename)


create_plot_figure([1,2,3,4], [5,6,7,8], "Test X", "Test Y", "trialPlot.png")

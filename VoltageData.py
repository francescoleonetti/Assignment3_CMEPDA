import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt

class VoltageData:

    """Class for managing a sequence of voltage measurements taken at 
    different times. 
    """

    def __init__(self, times, voltages):
        """Class constructor. Times and voltages are iterables of the same 
        lenght.
        """
        times = np.array(times, dtype=np.float64)
        voltages = np.array(voltages, dtype=np.float64)
        self.data = np.column_stack([times, voltages])
        self._spline = interpolate.InterpolatedUnivariateSpline(times, voltages, k =3)

    @classmethod
    def from_file(cls, data_path):
        """Constructor from a file
        """
        times, voltages = np.loadtxt(data_path, unpack=True)
        return cls(times, voltages)

    @property 
    def times(self):
        return self.data[:, 0]

    @property
    def voltages(self):
        return self.data[:, 1]

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __str__(self):
        header = 'Row -> Time [s], Voltage [mV]\n'
        return header + '\n'.join([f'{i} -> {row[0]: .1f}, {row[1]: .2f}' \
            for i, row in enumerate(self)])

    def __repr__(self):
        return '\n'.join([f'{row[0]} {row[1]}' for row in self])

    def __call__(self, t):
        return self._spline(t)

    def plot(self, ax=None, draw_spline=False, **plot_opts):
        if ax is None:
            plt.figure('voltage_vs_time')
        else:
            plt.sca(ax)
        plt.plot(self.times, self.voltages, label='data', **plot_opts)
        if draw_spline:
            x = np.linspace(min(self.times), max(self.times), 1000)
            plt.plot(x, self(x), '-', label='spline', color='darkorange')
        plt.xlabel('Time[s]')
        plt.ylabel('Voltage [mV]')
        plt.legend()
        plt.grid(True)           











if __name__ == '__main__':

    vdata = VoltageData.from_file('/Users/franc/Desktop/DISPENSE 4 ANNO/Computing Methods/Assignment3_CMEPDA/data.txt')

    print(vdata.times)
    print(vdata.voltages)

    print(vdata[3, 1])
    print(vdata[1:5, 0])

    print(len(vdata))

    for element in vdata:
        print(element)

    print(vdata)
    print(repr(vdata))

    print(vdata(0.63))

    vdata.plot(marker='o', linestyle='--', color='blue', draw_spline=True)
    plt.show()

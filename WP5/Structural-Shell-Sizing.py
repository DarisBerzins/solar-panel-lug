import numpy as np
import matplotlib.pyplot as plt

'''IDEAS:
- 
'''

'''ASSUMPTIONS:
- Shell is thin walled
- Constant thickness
'''

class Shell:
    def __init__(self, length, diameter, E_modulus, density, initial_thickness):
        self.length = length
        self.diameter = diameter
        self.E_modulus = E_modulus
        self.thickness = initial_thickness
        self.density = density
        self.masses = np.empty((0, 2), float)
        self.acceleration = 9.81
        self.total_mass = 2 * np.pi * (self.diameter / 2) * self.thickness * self.length * self.density * self.acceleration
        self.heights = np.array([])
        self.loads_above = np.array([])
    def add_mass(self, mass, height_position):
        '''Adds a mass at a height position'''
        self.masses = np.append(self.masses, [[mass, height_position]], axis=0)

    def add_mass_position_array(self, mass_position_array):
        '''Takes an array with elements [Mass, Height of application]'''
        self.masses = np.array(mass_position_array)

    def set_acceleration(self, acceleration):
        '''Sets the acceleration the part is subjected to'''
        self.acceleration = acceleration
        self.total_mass = 2 * np.pi * (self.diameter / 2) * self.thickness * self.length * self.density

    def get_loads(self, resolution):
        '''Gets the loads above a certain height'''
        self.heights = np.linspace(0, self.length, resolution)
        self.loads_above = np.zeros_like(self.heights)
        for i, height in enumerate(self.heights):
            total_mass_above = np.sum(self.masses[self.masses[:, 1] > height, 0])
            total_mass_above += self.total_mass * ((self.length - height) / self.length)
            self.loads_above[i] = total_mass_above * self.acceleration
    def get_maxload(self, resolution):
        self.get_loads(resolution)
        return self.loads_above.max()
    def plot_normal_stress_diagram(self, resolution):
        '''Plots the normal stress diagram in acceleration of the shell at the given resolution'''
        self.get_loads(resolution)
        # Plotting the load diagram
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(self.loads_above, self.heights, label='Load Above', color='b')
        ax.fill_betweenx(self.heights, self.loads_above, color='b', alpha=0.3)  # Shading the area
        ax.set_xlabel('Load (N)', labelpad=15, fontsize=14)
        ax.set_ylabel('Height (m)', labelpad=15, fontsize=14)
        ax.set_title('Normal Stress Diagram')
        ax.legend()
        ax.grid(False)

        # Centering x and y axes at zero and making them thicker
        ax.spines['left'].set_position('zero')
        ax.spines['left'].set_linewidth(2)
        ax.spines['left'].set_color('black')
        ax.spines['bottom'].set_position('zero')
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['bottom'].set_color('black')

        # Removing the top and right spines (outline)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        # Adding labels to the axes themselves
        ax.xaxis.set_label_position('bottom')
        ax.yaxis.set_label_position('left')

        plt.show()
    def get_safety_margin(self, allowed, real):
    def find_column_buckling_thickness(self):
        R = self.diameter/2
        sigmacr = (np.power(np.pi, 2)*self.E_modulus*0.5*np.pi*np.power(R, 4)*np.power((R-self.thickness), 4))/(2*np.pi*R*self.thickness)
        sigmareal = shell.get_maxload(1000)/(2*np.pi*R*self.thickness)
        SM = shell.get_safety_factor(sigmacr, sigmareal)
        '''finds the needed thickness of the shell to resist column buckling'''
    def find_shell_buckling_thickness(self):
        '''finds the needed thickness of the shell to resist shell buckling'''

# TESTING --------------------------------------------------------
shell = Shell(length=10, diameter=1, E_modulus=210e9, density=785, initial_thickness=0.1)
shell.set_acceleration(9.81*9)
shell.add_mass_position_array([[1000, 2], [1500, 4], [2000, 6], [2500, 8]])
shell.plot_normal_stress_diagram(resolution=10000)

import numpy as np
import matplotlib.pyplot as plt

'''IDEAS:
- Multiple shells one on top of the other with different thicknesses can reduce weight
- Variable thicknesses for different cylinder sections
- Contrain is not column buckling --> For it to be optimized you need a tiny diameter
- We size the diameter based on the tank size
- Also limited by bending stiffness for diameter, AMOI
- Argue that using the max compression is not reasonable since buckling assumes constant force distribution and is geometry dependent --> Cannot be applied to a point
- Hopefully argue that the moment tension/compression is sufficiently small to be included within the safety factor
- Say that we can pressurize it such that we control tension. Pressurized during launch and vented when in zero G
'''

'''ASSUMPTIONS:
- Shell is thin walled
- Constant thickness
- Only loads considered are point load masses and shell distributed weight mass
'''

class Shell:
    def __init__(self, length, diameter, E_modulus, density, initial_thickness, poisson_ratio):
        self.length = length
        self.diameter = diameter
        self.E_modulus = E_modulus
        self.thickness = initial_thickness
        self.density = density
        self.masses = np.empty((0, 4), float)
        self.acceleration = 9.81
        self.total_weight = 2 * np.pi * (self.diameter / 2) * self.thickness * self.length * self.density * self.acceleration
        self.heights = np.array([])
        self.loads_above = np.array([])
        self.poisson_ratio = poisson_ratio
    def add_mass(self, mass, height_position, x, y):
        '''Adds a mass at a height position'''
        self.masses = np.append(self.masses, [mass, height_position, x, y], axis=0)

    def add_mass_position_array(self, mass_position_array):
        '''Takes an array with elements [Mass, Height of application,x, y]'''
        self.masses = np.array(mass_position_array)

    def set_acceleration(self, acceleration):
        '''Sets the acceleration the part is subjected to'''
        self.acceleration = acceleration
        self.total_weight = 2 * np.pi * (self.diameter / 2) * self.thickness * self.length * self.density

    def get_loads(self, resolution):
        '''Gets the loads above a certain height'''
        self.heights = np.linspace(0, self.length, resolution)
        self.loads_above = np.zeros_like(self.heights)
        self.moments_x_above = np.zeros_like(self.heights)
        self.moments_y_above = np.zeros_like(self.heights)
        for i, height in enumerate(self.heights):
            total_mass_above = np.sum(self.masses[self.masses[:, 1] > height, 0])
            total_mass_above += self.total_weight * ((self.length - height) / self.length)
            self.moments_x_above[i] = np.sum(np.multiply(self.masses[self.masses[:, 1] > height, 0], self.masses[self.masses[:, 1] > height, 2]*self.acceleration))
            self.moments_y_above[i] = np.sum(np.multiply(self.masses[self.masses[:, 1] > height, 0], self.masses[self.masses[:, 1] > height, 3]*self.acceleration))
            self.loads_above[i] = total_mass_above * self.acceleration
        self.moment_magnitudes = np.sqrt(np.power(self.moments_x_above,2) + np.power(self.moments_y_above,2))
    def get_maxload(self, resolution):
        self.get_loads(resolution)
        return self.loads_above.max()

    def plot_normal_stress_diagram(self, resolution):
        '''Plots the normal stress (N), moments (M_x and M_y) diagram of the shell at the given resolution'''
        self.get_loads(resolution)

        # Plotting the diagrams
        fig, ax1 = plt.subplots(figsize=(12, 8))

        # Plotting Load Above
        ax1.plot(self.loads_above, self.heights, label='Normal load (N)', color='b')
        ax1.fill_betweenx(self.heights, self.loads_above, color='b', alpha=0.3)  # Shading for loads
        ax1.set_xlabel('Load (N)', labelpad=15, fontsize=14, color='b')
        ax1.set_ylabel('Height (m)', labelpad=15, fontsize=14)
        ax1.tick_params(axis='x', labelcolor='b')
        ax1.set_title('Normal, Shear, and Moment Diagram (NVM)', fontsize=16)

        # Adding a secondary axis for Moments
        ax2 = ax1.twiny()
        ax2.plot(self.moments_x_above, self.heights, label='Moment X (Nm)', color='r', linestyle='--')
        ax2.plot(self.moments_y_above, self.heights, label='Moment Y (Nm)', color='g', linestyle='--')
        ax2.plot(self.moment_magnitudes, self.heights, label='Moment Magnitude (Nm)')
        ax2.set_xlabel('Moment (Nm)', labelpad=15, fontsize=14)
        ax2.tick_params(axis='x', colors='r')

        # Legends and grid
        fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
        ax1.grid(False)

        # Centering x and y axes at zero and making them thicker
        ax1.spines['left'].set_position('zero')
        ax1.spines['left'].set_linewidth(2)
        ax1.spines['left'].set_color('black')
        ax1.spines['bottom'].set_position('zero')
        ax1.spines['bottom'].set_linewidth(2)
        ax1.spines['bottom'].set_color('black')

        # Removing the top and right spines for primary and secondary axes
        ax1.spines['right'].set_color('none')
        ax1.spines['top'].set_color('none')
        ax2.spines['bottom'].set_color('none')

        # Adding labels for clarity
        ax1.xaxis.set_label_position('bottom')
        ax1.yaxis.set_label_position('left')
        ax2.xaxis.set_label_position('top')

        plt.show()

    def get_safety_factor(self, allowed, real):
        return allowed / real
    def find_column_buckling_thickness(self, initial_thickness, margin=np.array([1.0, 1.05]), maxit=10000):
        '''finds the needed thickness of the shell to resist column buckling'''
        R = self.diameter/2
        iterthickness = initial_thickness
        SM = margin[0] - 0.5
        i=0
        while SM < margin[0] or SM > margin[1]:
            sigmacr = (np.power(np.pi, 2)*self.E_modulus*0.5*np.pi*(np.power(R, 4)-np.power((R-iterthickness), 4)))/(2*np.pi*R*iterthickness)
            sigmareal = self.get_maxload(1000)/(2*np.pi*R*iterthickness)
            SM = self.get_safety_factor(sigmacr, sigmareal)
            iterthickness = iterthickness/SM
            i+=1
            if i > maxit:
                print('Maximum iteration read')
                break
        return iterthickness
    def find_shell_buckling_thickness(self, pressure,initial_thickness, margin=np.array([1.0, 1.05]), maxit=10000):
        '''finds the needed thickness of the shell to resist shell buckling'''
        SM = margin[1] + 1
        R = self.diameter / 2
        iterthickness = initial_thickness
        i=0
        while SM < margin[0] or SM > margin[1]:
            sigmacr = self.get_shell_buckling_critical(iterthickness, pressure)
            sigmareal = shell.get_maxload(1000)/(2*np.pi*R*iterthickness)
            SM = self.get_safety_factor(sigmacr, sigmareal)
            iterthickness = iterthickness/SM
            i+=1
            if i > maxit:
                print('Maximum iteration read')
                break
        return iterthickness

    def find_lambda(self, thickness):
        return np.sqrt((12*(self.length**4)*(1-(self.poisson_ratio**2)))/((np.pi**4)*((self.diameter/2)**2)*(thickness**2)))

    def get_shell_buckling_critical(self, thickness, pressure):
        Q = (pressure/self.E_modulus)*(((self.diameter/2)/thickness)**2)
        lambda_val = self.find_lambda(thickness)
        k = lambda_val + (12 / np.pi ** 4) * (self.length ** 4 / ((self.diameter/2) ** 2 * thickness ** 2)) * (1 - self.poisson_ratio ** 2) / lambda_val
        critical_sigma = k*(1.983 - (0.983 * np.exp(-23.14 * Q)))*(((np.pi**2)*self.E_modulus)/(12*(1-(self.poisson_ratio**2))))*((thickness/self.length)**2)
        return critical_sigma

    def find_thickness_convolution(self, thickness, pressure):
        weightdiff = 10
        self.thickness = thickness
        while weightdiff >= 0.0001:
            weight = self.total_weight
            self.thickness_shell = self.find_shell_buckling_thickness(pressure, self.thickness)
            self.thickness_buckling = self.find_column_buckling_thickness(self.thickness)
            self.thickness = max(self.thickness_shell, self.thickness_buckling)
            self.total_weight = 2 * np.pi * (self.diameter / 2) * self.thickness * self.length * self.density * self.acceleration
            weightdiff = abs(weight - self.total_weight)
        return self.thickness, self.thickness_shell, self.thickness_buckling

    def find_radius_convolution(self, thickness, pressure):
        CF = 10
        while CF < 0.99 or CF > 1.01:
            thickness, thickness_shell, thickness_buckling = self.find_thickness_convolution(thickness, pressure)
            CF = thickness_shell/thickness_buckling
            self.diameter = self.diameter/CF
            print(self.diameter)
        return self.diameter, thickness
    def plot_n_find_thickness_ratio(self, pressure, diameter_range=None, subdivisions=5, initial_thickness=0.0001):
        if diameter_range is None:
            diameter_range = np.array([0.07, 0.1])
        diameters = np.linspace(diameter_range[0], diameter_range[1], subdivisions)
        thickness_ratios = np.empty_like(diameters)
        i=0
        for diameter in diameters:
            self.diameter = diameter
            thickness, thickness_shell, thickness_buckling = self.find_thickness_convolution(initial_thickness, pressure)
            thickness_ratio = thickness_shell/thickness_buckling
            thickness_ratios[i] = thickness_ratio
            i+=1
            print(thickness_shell, thickness_buckling,thickness_ratio)
        plt.plot(diameters, thickness_ratios)
        plt.grid(True)
        plt.show()
        print("Mass of last element is ", (self.total_weight/self.acceleration), "kg")
    def compare_weight_n_bending_tensions(self):
        R=self.diameter/2
        weight_tension = self.total_weight/(2*np.pi*R*self.thickness)



# TESTING --------------------------------------------------------
shell = Shell(length=4, diameter=0.805, E_modulus=73.1e9, density=785, initial_thickness=0.1, poisson_ratio=0.33)
shell.set_acceleration(9.81*20)
shell.add_mass_position_array([[100, 1, 1, 1], [150, 2, 1, 0], [200, 3, 0, 1], [250, 3.5, 0.5,0.5]])
shell.plot_normal_stress_diagram(resolution=10000)

#shell.plot_n_find_thickness_ratio(15000)
# print("Iterated thickness: ", shell.find_radius_convolution(0.1, 15000))
# print(shell.find_thickness_convolution(0.1,50))
# print(shell.find_thickness_convolution(0.1,100))
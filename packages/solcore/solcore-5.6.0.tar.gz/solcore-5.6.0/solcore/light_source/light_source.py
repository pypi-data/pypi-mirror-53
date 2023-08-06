import os
from scipy.interpolate import interp1d
import numpy as np

from solcore.science_tracker import science_reference
from solcore import spectral_conversion_nm_ev, spectral_conversion_nm_hz, eVnm, nmHz, nmJ
from solcore.constants import q, h, c, kb

from solcore.light_source.spectral2 import get_default_spectral2_object, calculate_spectrum_spectral2
from solcore.light_source.smarts import get_default_smarts_object, calculate_spectrum_smarts


def reference_spectra():
    """ Function providing the standard reference spectra: AM0, AM1.5g and AM1.5d.

    :return: A 2D array with 4 columns representing the wavelength, AM0, AM1.5g and AM1.5d standard spectra."""

    science_reference("Standard solar spectra",
                      "ASTM G173-03(2012), Standard Tables for Reference Solar Spectral Irradiances: "
                      "Direct Normal and Hemispherical on 37° Tilted Surface, ASTM International, "
                      "West Conshohocken, PA, 2012, www.astm.org")

    this_dir = os.path.split(__file__)[0]
    output = np.loadtxt(os.path.join(this_dir, "astmg173.csv"), dtype=float, delimiter=',', skiprows=2)

    return output


class LightSource:
    """ This is a common interface to access all types of light sources supported by Solcore: standard solar spectra (AM0, AM1.5g, and AM1.5d), blackbody radiation, laser light or spectra created from atmospheric data using SPECTRAL2 or SMARTS. Aditionally, it can also use experimentally measured spectra.
    """
    type_of_source = ['laser', 'black body', 'standard', 'SMARTS', 'SPECTRAL2', 'custom']
    output_units = ['power_density_per_eV', 'power_density_per_nm', 'power_density_per_J',
                    'power_density_per_m', 'power_density_per_hz', 'photon_flux_per_eV', 'photon_flux_per_nm',
                    'photon_flux_per_J', 'photon_flux_per_hz', 'photon_flux_per_m']

    def __init__(self, source_type, x=None, **kwargs):
        """

        :param source_type:
        :param kwargs:
        """
        self.source_type = source_type
        self.x = x
        self.x_internal = x
        self.power_density = 0

        self.options = {'output_units': 'power_density_per_nm', 'concentration': 1}
        self.options.update(kwargs)

        self._update_get_spectrum()
        self._update_spectrum_function()

        self.ready = False
        self.cache_spectrum = None

    def spectrum(self, x=None, **kwargs):
        """ Returns the spectrum of the light in the requested units. Internally, the spectrum is always managed in power density per nanometers, but the output can be provided in other compatible units, such as power density per Hertz or photon flux per eV.

        :param x: (Default=None) If "x" is provided, it must be an array with the spectral range in which to calculate the spectrum. Depending on the "units" defined when creating the light source, this array must be in nm, m, eV, J or hz.
        :param kwargs: Options to update the light source. It can be "units", "concentration" or any of the options specific to the chosen type of light source.
        :return: Array with the spectrum in the requested units
        """
        if x is not None:
            self.x = x
            self.ready = False

        try:
            if len(kwargs) > 0:
                self._update(**kwargs)
                self._update_spectrum_function()
                output = self._get_spectrum(self.x)
                self.cache_spectrum = output
            elif not self.ready:
                self._update_spectrum_function()
                output = self._get_spectrum(self.x)
                self.cache_spectrum = output
            else:
                output = self.cache_spectrum

            return self.x, output * self.options['concentration']

        except Exception as err:
            print('ERROR: No stored spectrum or "x" data not available.'
                  'You must call the "spectrum" function at least once with a value for the "x" argument.')
            print(err)

    def _update(self, **kwargs):
        """ Updates the options of the light source with new values. It only updates existing options. No new options are added.

        :param kwargs: A dictionary with the options to update and their new values.
        :return: None
        """

        for opt in kwargs:
            if opt in self.options:
                self.options[opt] = kwargs[opt]

        if 'output_units' in kwargs:
            self._update_get_spectrum()

        self.ready = False
        self.cache_spectrum = None

    def _update_get_spectrum(self):
        """ Updates the function to get the spectrum, depending on the chosen output units.

        :return: None
        """

        try:
            units = self.options['output_units']

            if units == 'power_density_per_nm':
                self._get_spectrum = self._get_power_density_per_nm
            elif units == 'power_density_per_m':
                self._get_spectrum = self._get_power_density_per_m
            elif units == 'photon_flux_per_nm':
                self._get_spectrum = self._get_photon_flux_per_nm
            elif units == 'photon_flux_per_m':
                self._get_spectrum = self._get_photon_flux_per_m
            elif units == 'power_density_per_eV':
                self._get_spectrum = self._get_power_density_per_eV
            elif units == 'photon_flux_per_eV':
                self._get_spectrum = self._get_photon_flux_per_eV
            elif units == 'power_density_per_J':
                self._get_spectrum = self._get_power_density_per_J
            elif units == 'photon_flux_per_J':
                self._get_spectrum = self._get_photon_flux_per_J
            elif units == 'power_density_per_hz':
                self._get_spectrum = self._get_power_density_per_hz
            elif units == 'photon_flux_per_hz':
                self._get_spectrum = self._get_photon_flux_per_hz
            else:
                raise ValueError('Unknown units: {0}.\nValid units are: {1}.'.format(units, self.output_units))

        except ValueError as err:
            print(err)

    def _get_power_density_per_nm(self, wavelength):
        """ Function that returns the spectrum in power density per nanometer.

        :param wavelength: Array with the wavelengths at which to calculate the spectrum (in nm)
        :return: The spectrum in the chosen units.
        """
        output = self._spectrum(wavelength)
        return output

    def _get_photon_flux_per_nm(self, wavelength):
        """ Function that returns the spectrum in photon flux per nanometer.

        :param wavelength: Array with the wavelengths at which to calculate the spectrum (in nm)
        :return: The spectrum in the chosen units.
        """
        output = self._spectrum(wavelength)
        output = output / (c * h * 1e+9 / wavelength)
        return output

    def _get_power_density_per_m(self, wavelength):
        """ Function that returns the spectrum in power density per meter.

        :param wavelength: Array with the wavelengths at which to calculate the spectrum (in m)
        :return: The spectrum in the chosen units.
        """
        output = self._spectrum(wavelength * 1e-9) * 1e9
        return output

    def _get_photon_flux_per_m(self, wavelength):
        """ Function that returns the spectrum in photon flux per meter.

        :param wavelength: Array with the wavelengths at which to calculate the spectrum (in m)
        :return: The spectrum in the chosen units.
        """
        output = self._spectrum(wavelength * 1e9)
        output = output / (c * h / wavelength) * 1e9
        return output

    def _get_power_density_per_eV(self, energy):
        """ Function that returns the spectrum in power density per eV.

        :param energy: Array with the energies at which to calculate the spectrum (in eV)
        :return: The spectrum in the chosen units.
        """
        wavelength = eVnm(energy)[::-1]
        output = self._spectrum(wavelength)
        energy_eV, output = spectral_conversion_nm_ev(wavelength, output)
        return output

    def _get_photon_flux_per_eV(self, energy):
        """ Function that returns the spectrum in photon flux per eV.

        :param energy: Array with the energies at which to calculate the spectrum (in eV)
        :return: The spectrum in the chosen units.
        """
        wavelength = eVnm(energy)[::-1]
        output = self._spectrum(wavelength)
        energy_eV, output = spectral_conversion_nm_ev(wavelength, output)
        output = output / (q * energy)
        return output

    def _get_power_density_per_J(self, energy):
        """ Function that returns the spectrum in power density per Joule.

        :param energy: Array with the energies at which to calculate the spectrum (in J)
        :return: The spectrum in the chosen units.
        """
        wavelength = nmJ(energy)[::-1]
        output = self._spectrum(wavelength)
        energy_eV, output = spectral_conversion_nm_ev(wavelength, output)
        output = output / q
        return output

    def _get_photon_flux_per_J(self, energy):
        """ Function that returns the spectrum in photon flux per Joule.

        :param energy: Array with the energies at which to calculate the spectrum (in J)
        :return: The spectrum in the chosen units.
        """
        wavelength = nmJ(energy)[::-1]
        output = self._spectrum(wavelength)
        energy_eV, output = spectral_conversion_nm_ev(wavelength, output)
        output = output / (q * energy)
        return output

    def _get_power_density_per_hz(self, frequency):
        """ Function that returns the spectrum in power density per hertz.

        :param frequency: Array with the frequencies at which to calculate the spectrum (in hz)
        :return: The spectrum in the chosen units.
        """
        wavelength = nmHz(frequency)[::-1]
        output = self._spectrum(wavelength)
        frequency, output = spectral_conversion_nm_hz(wavelength, output)
        return output

    def _get_photon_flux_per_hz(self, frequency):
        """ Function that returns the spectrum in photon flux per hertz.

        :param frequency: Array with the frequencies at which to calculate the spectrum (in hz)
        :return: The spectrum in the chosen units.
        """
        wavelength = nmHz(frequency)[::-1]
        output = self._spectrum(wavelength)
        frequency, output = spectral_conversion_nm_hz(wavelength, output)
        output = output / (h * frequency)
        return output

    def _update_spectrum_function(self):
        """ Updates the spectrum function during the light source creation or just after updating one or more of the options. It also updates the "options" property with any default options available to the chosen light source, if any.

        :return: True
        """
        try:
            if self.source_type == 'standard':
                self._spectrum = self._get_standard_spectrum(self.options)
            elif self.source_type == 'laser':
                self._spectrum = self._get_laser_spectrum(self.options)
            elif self.source_type == 'black body':
                self._spectrum = self._get_blackbody_spectrum(self.options)
            elif self.source_type == 'SPECTRAL2':
                self._spectrum = self._get_spectral2_spectrum(self.options)
            elif self.source_type == 'SMARTS':
                self._spectrum = self._get_smarts_spectrum(self.options)
            elif self.source_type == 'custom':
                self._spectrum = self._get_custom_spectrum(self.options)
            else:
                raise ValueError('Unknown type of light source: {0}.\nValid light sources are: {1}'.format(
                    self.source_type, self.type_of_source))

            self.ready = True

        except ValueError as err:
            print(err)

    def _get_standard_spectrum(self, options):
        """ Gets one of the reference standard spectra: AM0, AM1.5g or AM1.5d.

        :param options: A dictionary that contains the 'version' of the standard spectrum: 'AM0', 'AM1.5g' or 'AM1.5d'
        :return: A function that takes as input the wavelengths and return the standard spectrum at those wavelengths.
        """

        try:
            version = options['version']

            spectra = reference_spectra()
            wl = spectra[:, 0]

            if version == 'AM0':
                spectrum = spectra[:, 1]
            elif version == 'AM1.5g':
                spectrum = spectra[:, 2]
            elif version == 'AM1.5d':
                spectrum = spectra[:, 3]
            else:
                raise KeyError('ERROR when creating a standard light source. Input parameters must include "version" '
                               'which can be equal to "AM0", "AM1.5g" or "AM1.5d" only.')

            self.x_internal = wl
            self.power_density = np.trapz(y=spectrum, x=wl) * self.options['concentration']
            output = interp1d(x=wl, y=spectrum, bounds_error=False, fill_value=0, assume_sorted=True)
            return output

        except KeyError as err:
            print(err)

    def _get_laser_spectrum(self, options):
        """ Creates a gaussian light source with a given total power, linewidth and central wavelength. These three parameters must be provided in the "options" diccionary.

        :param options: A dictionary that must contain the 'power', the 'linewidth' and the 'center' of the laser emission.
        :return: A function that takes as input the wavelengths and return the laser spectrum at those wavelengths.
        """
        try:
            power = options['power']
            sigma2 = options['linewidth'] ** 2
            center = options['center']

            def output(x):
                out = power / np.sqrt(2 * np.pi * sigma2) * np.exp(- (x - center) ** 2 / 2 / sigma2)
                return out

            self.x_internal = np.arange(center - 5 * options['linewidth'], center + 5 * options['linewidth'],
                                        options['linewidth'] / 20)
            self.power_density = power * self.options['concentration']
            return output

        except KeyError:
            print('ERROR when creating a laser light source. Input parameters must include "power", "linewidth"'
                  ' and "center".')

    def _get_blackbody_spectrum(self, options):
        """ Gets the expontaneous emission in W/m2/sr/nm from a black body source chemical potential = 0

        :param options: A dictionary that must contain the temperature of the blackbody, in kelvin 'T' and the 'entendue' in sr. If not provided, the entendue will be taken as 1 sr. Possible values for entendue are:
            - 'Sun': The entendue will be taken as 6.8e-5 sr.
            - 'hemispheric': The entendue wil be taken as pi/2 sr.
            - A numeric value
        :return: A function that takes as input the wavelengths and return the black body spectrum at those wavelengths.
        """

        try:
            T = options['T']
            if 'entendue' in options:
                if options['entendue'] == 'Sun':
                    entendue = 6.8e-5
                elif options['entendue'] == 'hemispheric':
                    entendue = np.pi / 2
                else:
                    entendue = options['entendue']
            else:
                entendue = 1
                options['entendue'] = 1

            def BB(x):
                x = x * 1e-9
                out = 2 * entendue * h * c ** 2 / x ** 5 / (np.exp(h * c / (x * kb * T)) - 1)
                return out * 1e-9

            wl_max = 2.8977729e6/T
            self.x_internal = np.arange(0, wl_max*10, wl_max/100)
            sigma = 5.670367e-8
            self.power_density = sigma * T ** 4 * entendue / np.pi * self.options['concentration']

            return BB

        except KeyError:
            print('ERROR when creating a blackbody light source. Input parameters must include "T" and, '
                  'optionally, an "entendue", whose values can be "Sun" "hemispheric" or a number. '
                  'Equal to 1 if omitted.')

    def _get_spectral2_spectrum(self, options):
        """ Get the solar spectrum calculated with the SPECTRAL2 calculator. The options dictionary is updated with the default options of all parameters if they are not provided.

        :param options: A dictionary that contain all the options for the calculator.
        :return: A function that takes as input the wavelengths and return the SPECTRAL2 calculated spectrum at those wavelengths.
        """
        default = get_default_spectral2_object()

        for opt in options:
            if opt in default:
                default[opt] = options[opt]

        options.update(default)

        wl, irradiance = calculate_spectrum_spectral2(options, power_density_in_nm=True)

        self.x_internal = wl
        self.power_density = np.trapz(y=irradiance, x=wl) * self.options['concentration']
        output = interp1d(x=wl, y=irradiance, bounds_error=False, fill_value=0, assume_sorted=True)
        return output

    def _get_smarts_spectrum(self, options):
        """ Get the solar spectrum calculated with the SMARTS calculator. The options dictionary is updated with the default options of all parameters if they are not provided.

        :param options: A dictionary that contain all the options for the calculator.
        :return: A function that takes as input the wavelengths and return the SMARTS calculated spectrum at those wavelengths.
        """
        outputs = {'Extraterrestial': 2, 'True direct': 2, 'Experimental direct': 3, 'Global horizontal': 4,
                   'Global tilted': 5}

        default = get_default_smarts_object()

        for opt in options:
            if opt in default:
                default[opt] = options[opt]

        options.update(default)

        if 'output' not in options:
            options['output'] = 'Global horizontal'

        try:
            output = outputs[options['output']]

            out = calculate_spectrum_smarts(options)

            self.x_internal = out[0]
            self.power_density = np.trapz(y=out[output], x=out[0]) * self.options['concentration']
            output = interp1d(x=out[0], y=out[output], bounds_error=False, fill_value=0, assume_sorted=True)
            return output

        except KeyError:
            print('ERROR: Output option no recognized. Avaliable options are: {}'.format(outputs))
        except RuntimeError as err:
            print('ERROR in SMARTS: {}'.format(err))

    def _get_custom_spectrum(self, options):
        """ Convert an custom spectrum into a solcore light source object.

        :param options: A dictionary that contains the following information:
            - 'x_data' and 'y_data' of the custom spectrum.
            - 'input_units', the units of the spectrum, such as 'photon_flux_per_nm' or 'power_density_per_eV'
        :return: A function that takes as input the wavelengths and return the custom spectrum at those wavelengths.
        """

        try:
            x_data = options['x_data']
            y_data = options['y_data']
            units = options['input_units']

            # We check the units type by type.
            # Regardless of the input, we want power_density_per_nm
            if units == 'power_density_per_nm':
                wl = x_data
                spectrum = y_data
            elif units == 'photon_flux_per_nm':
                wl = x_data
                spectrum = y_data * (c * h * 1e+9 / wl)
            elif units == 'power_density_per_eV':
                wl, spectrum = spectral_conversion_nm_ev(x_data, y_data)
            elif units == 'photon_flux_per_eV':
                wl, spectrum = spectral_conversion_nm_ev(x_data, y_data)
                spectrum = spectrum * (c * h * 1e+9 / wl)
            elif units == 'power_density_per_J':
                wl, spectrum = spectral_conversion_nm_ev(x_data / q, y_data * q)
            elif units == 'photon_flux_per_J':
                wl, spectrum = spectral_conversion_nm_ev(x_data / q, y_data * q)
                spectrum = spectrum * (c * h * 1e+9 / wl)
            elif units == 'power_density_per_hz':
                wl, spectrum = spectral_conversion_nm_hz(x_data, y_data)
            elif units == 'photon_flux_per_hz':
                wl, spectrum = spectral_conversion_nm_hz(x_data, y_data)
                spectrum = spectrum * (h * x_data)
            else:
                raise ValueError('Unknown units: {0}.\nValid units are: {1}.'.format(units, self.output_units))

            self.x_internal = wl
            self.power_density = np.trapz(y=spectrum, x=wl) * self.options['concentration']
            output = interp1d(x=wl, y=spectrum, bounds_error=False, fill_value=0, assume_sorted=True)
            return output

        except KeyError as err:
            print(err)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    plt.figure(figsize=(6, 4.5))

    # The wavelength range of the spectra
    wl = np.linspace(300, 3000, 200)

    gauss = LightSource(source_type='laser', x=wl, center=800, linewidth=50, power=200)
    bb = LightSource(source_type='black body', x=wl, T=5800, entendue='Sun')
    am15g = LightSource(source_type='standard', x=wl, version='AM1.5g')
    smarts = LightSource(source_type='SMARTS', x=wl)
    spectral = LightSource(source_type='SPECTRAL2', x=wl)

    plt.plot(*gauss.spectrum(), label='Gauss')
    plt.plot(*bb.spectrum(), label='Black body')
    plt.plot(*am15g.spectrum(), label='AM1.5G')
    plt.plot(*smarts.spectrum(), label='SMARTS')
    plt.plot(*spectral.spectrum(), label='SPECTRAL2')

    plt.xlim(300, 3000)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Power density (Wm$^{-2}$nm$^{-1}$)')
    plt.tight_layout()
    plt.legend(frameon=False)

    plt.show()

import numpy as np
from scipy.signal import find_peaks

class OptDevice:
    '''Parent class for a device'''

    def __init__(self, ports: list):
        '''
        Init the device:

        :param ports: ports list the device is connected to
        
        '''
        self.ports = ports

    def __repr__(self):
        """
        String representation of the optical device.
        """
        return f"<OptDevice, ports = {self.ports}>"


class AddDropMRR(OptDevice):
    '''Simulation of a Microring resonator'''

    def __init__(self, port_T: int, port_D: int, r1: float = None, r2: float = None, 
                 a: float = None, R: float = None, neff: float = None, lam: list[int] = None): 
        """
        Initialize the MRM: ↓

        :param port_T: port Thru
        :param port_D: port Drop
        :param r1: self-coupling coefficient for Input-Thru waveguide/MRR coupling
        :param r2: self-coupling coefficient for Drop-Prt waveguide/MRR coupling
        :param a: roundtrip loss
        :param R:  radius of the MRR in meters
        :param neff: effective refractive index
        :param lam: wavelength range in meters

        MRR illustration: ↓ 
        
          <- Drop [E8]               Prt
            ____________________________
                   ┌───────────┐
                   |           │
                   │   ┌───┐   │
                   │   │   │   │
                   |   └───┘   |
                   │           │
                   └───────────┘
            ____________________________
         -> Input [E1]             ->Through [E2] 
    
        Fields: ↓ 
        [E2] = T x [E1]
        [E8] = D x [E1]
        
        Return the scattering final equations T and D from the S-matrix analysis 
        that relate electric fields [E1] with [E2, E8] at the output ports.

        """
        super().__init__(ports=[port_T, port_D])
        
        self.port_T = port_T
        self.port_D = port_D

        # Assigned to typical values if unspecified:
        if r1 is None: r1 = 0.9816
        if r2 is None: r2 = 0.9816
        if a is None: a = 0.9816
        if R is None: R = 8000.0e-9
        if neff is None: neff = 10000*[3.505]
        if lam is None: lam = np.linspace(1558.0e-9,1560e-9,10000)

        self.r1 = r1
        self.r2 = r2
        self.a = a
        self.R = R
        self.neff = neff
        self.lam = lam
        
        phi = (4.0*neff*(np.pi**2.0)*R)/lam
        T = (r1 - r2*a*np.exp(1j*phi))/(1 - r1*r2*a*np.exp(1j*phi)) 
        D = ((np.sqrt((1-r1**2.0)*(1-r2**2.0)*a))*np.exp(1j*phi/2.0) )/(1-r1*r2*a*np.exp(1j*phi)) 

        self.S_params = [T, D]
        
    def get_S_params(self):
        """
        :return: A 1D numpy array with [T, D].
        """
        self.S_params = np.array(self.S_params, dtype=np.complex128)
        
        return self.S_params

    def propagate(self, input_field: complex):
        """
        Propagate input electric fields through the MRM.

        :param input_fields: The electric field at the input port E_1.
        :return: A 1D numpy array with the electric fields at the output ports [E2, E8].
        """
        if not isinstance(input_field, complex):
            raise ValueError(f"The input field must be a complex number, got {type(input_field).__name__}.")

        # Calculate the output fields [E2,E8] using the MRM_S
        [E8, E2] = self.get_S_params() * input_field * 1/np.sqrt(2)
        
        # Explicitly assign ports to the output fields
        return {self.port_T: E2, self.port_D: E8}

    def __repr__(self):
        """
        String representation of the MRR's ports.
        """
        return (f"<MRR: port_T={self.port_T}, port_D={self.port_D}, "
                f"r1={self.r1}, r2={self.r2}, a={self.a}, "
                f"R={self.R}, neff={self.neff}, lam={self.lam}>")



# Define num_MRR laser wavelemgths for the Balanced Photodetector
def BPD_output(num_MRR, lambda_original, lamdba_array: list[int] = None, I_E_T: list[int] = None, I_E_D: list[int] = None):

    # Check if the lengths match
    if len(lamdba_array) != num_MRR:
        raise ValueError(f"Error: Mismatch in length! Expected {num_MRR} elements but got {len(lamdba_array)} in laser_wavelengths.")

    
    peaks_yes,_ = find_peaks(I_E_D, height=(0.5,1))  
    
    if lamdba_array is None: 
        peaks = peaks_yes
        lam_P = [lambda_original[peaks][i] for i in range(len(peaks))] 
        #find peaks for T: resonance
        I_E_T_P = [I_E_T[peaks][i] for i in range(len(peaks))]
        #find peaks for D: resonance
        I_E_D_P = [I_E_D[peaks][i] for i in range(len(peaks))]
    
        # Output of the balanced photodiode
        Delta_I_E = I_E_D - I_E_T
        #find peaks for BPD: 
        Delta_I_E_P = [Delta_I_E[peaks][i] for i in range(len(peaks))]
    else:
        lamdba_array = np.array(lamdba_array)*1e9
        lambda_original = np.round(lambda_original*1e9,2)
        # Find indices where values change
        change_indices = np.insert(np.diff(lambda_original) != 0, 0, True)  # Always keep the first value
        # Select only the first occurrence of each sequence
        filtered = lambda_original[change_indices]
        lambda_original_ = filtered
        
        # Find the closest indices for each laser wavelength
        peaks = [np.abs(lambda_original_  - lw).argmin() for lw in lamdba_array]
        lam_P = [lambda_original_[peaks][i] for i in range(len(peaks))] 

        idx_array = np.linspace(0,len(lambda_original),len(lambda_original), dtype=int)
        idx_array_f = idx_array[change_indices]
        peakso = [idx_array_f[peaks][i] for i in range(len(peaks))] 
        #find peaks for T: resonance
        I_E_T_P = [I_E_T[peakso][i] for i in range(len(peakso))]
        #find peaks for D: resonance
        I_E_D_P = [I_E_D[peakso][i] for i in range(len(peakso))]
    
        # Output of the balanced photodiode
        Delta_I_E = I_E_D - I_E_T
        #find peaks for BPD: 
        Delta_I_E_P = [Delta_I_E[peakso][i] for i in range(len(peakso))]

    return I_E_T, I_E_T, I_E_T_P, I_E_D_P, Delta_I_E, Delta_I_E_P, lam_P, peaks,lambda_original_

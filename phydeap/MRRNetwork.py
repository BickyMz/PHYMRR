import numpy as np

from phydeap.PhotonicDevices import OptDevice, AddDropMRR

class MRR_Network(OptDevice):
    """Simulation of a microring resonator array"""

    def __init__(self, port_T: int, port_D: int, num_MRR: int, input_field: complex, 
                 n_idx: float, Lw: float, **params):
        """
        MRR array illustration: ↓
        
              <- Drop 
              ____________________________________________________________ . . . 
                   ┌───────────┐    ┌───────────┐    ┌───────────┐
                   |           │    |           │    |           │
                   │   ┌───┐   │    │   ┌───┐   │    │   ┌───┐   │
                   │   │   │   │    │   │   │   │    │   │   │   │         . . .
                   │   └───┘   │    │   └───┘   │    │   └───┘   │
                   │           │    │           │    │           │
                   └───────────┘    └───────────┘    └───────────┘
             _____________________________________________________________ . . . 
             -> Input                                            -> Through
             
        :param port_T: Thru port.
        :param port_D: Drop port.
        :param num_MRR: Number of microring resonators in the cascade.
        :param input_field: Complex input field.
        :param params: Additional parameters as keyword arguments, stored in the Params dictionary.
        :param n_idx: refractive index for waveguides interconnects. It doesn't change.
        :param Lw: tiny spacing between Thru/input waveguides (beyond the ring diameter) in meters.
        """

        super().__init__(ports=[port_T, port_D])
        
        self.port_T = port_T
        self.port_D = port_D
        self.num_MRR = num_MRR
        self.input_field = input_field
        self.Lw = Lw
        self.n_idx = n_idx
        self.params = params

    def get_S_params(self):

        self.lam_spacing = np.mean([self.params["MRR"+str(i)][-1] for i in range(self.num_MRR)])

        #Define phases:
        self.Theta_b = (2*np.pi*self.Lw*self.n_idx)/self.lam_spacing  #phase for spacing between MRRs Drop Waveguide
        self.Theta_t = self.Theta_b #phase for spacing between MRRs Thru Waveguide

        #method to define T1,T2,T3,....,D1,D2,D3,.....
        self.MRR_array_TD = np.array([AddDropMRR(*self.params['MRR'+str(i)]).get_S_params()
                                      for i in range(self.num_MRR)], dtype=np.complex128)
        #Thru Transmission for N rings
        self.S11_N = 1.0
        # Vectorized computation for the Thru port
        self.S11_N *= np.cumprod(self.MRR_array_TD[:,0,:] * np.exp(1j * self.Theta_b), axis=0)
        self.S11_N = self.S11_N[self.num_MRR-1,:]     
        
        #r2 values 
        r2_N = [self.params["MRR"+str(i)][4] for i in range(self.num_MRR)]
        #Drop Transmission for N rings 
        self.S12_N = 0.0
        for k in range(self.num_MRR):    
            temp = ((-1)**(k+1))*self.MRR_array_TD[k,1,:]
            for m in range(0,k):
                temp = temp * r2_N[m]*self.MRR_array_TD[m,0,:]*np.exp(1j*(m+1)*(self.Theta_t+ self.Theta_b))
            self.S12_N = self.S12_N + temp

        self.S_params = np.array([self.S11_N, self.S12_N])
        
        return self.S_params

    def propagate(self, input_field: complex):
        """
        Propagate input electric fields through the MRM.

        :param input_fields: The electric field at the input port E_1.
        :return: A 1D numpy array with the electric fields at the output ports [E_T, E_D].
        """
        if not isinstance(input_field, complex):
            raise ValueError(f"The input field must be a complex number, got {type(input_field).__name__}.")

        # Calculate the output fields [E2,E8] using the MRM_S
        [E_T, E_D] = self.get_S_params() * input_field *  1 / np.sqrt(2) 
        
        # Explicitly assign ports to the output fields
        return {self.port_T: E_T, self.port_D: E_D}

    def __repr__(self):
        """
        String representation of the MRR's ports.
        """
        return (f"<MRR: port_T={self.port_T}, port_D={self.port_D}, "
                f"num_MRR={self.num_MRR}, Lw={self.Lw}, n_idx={self.n_idx}")
    


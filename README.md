# PHYMRR


![MRR Diagram](https://github.com/BickyMz/PHYMRR/blob/main/images/MRR_WB.png)

<p align="center"> <h1> A Physical level simulation of a simple MRM and DEAP arrays </h1> </p>

<h3> The code implements variations of this circuit: </h3>


```
MRR array illustration: ↓                                                    Drop ->     ____
                                                _______________________________________ | PD |
                                               | <- Drop                                |____|  
                                        . . .  |________________________________          |
       ┌───────────┐    ┌───────────┐          ┌───────────┐    ┌───────────┐             |
       |           │    |           │          |           │    |           │             |
       │   ┌───┐   │    │   ┌───┐   │          │   ┌───┐   │    │   ┌───┐   │             O---> BPD ~ (Drop - Through)
       │   │   │   │    │   │   │   │  . . .   │   │   │   │    │   │   │   │  . . .      |
       │   └───┘   │    │   └───┘   │          │   └───┘   │    │   └───┘   │             |
       │           │    │           │          │           │    │           │             |
       └───────────┘    └───────────┘          └───────────┘    └───────────┘            ____
    ___________________________________ . . . _________________________________________ | PD |
                                                                                        |____|
    -> Input                                                                 -> Through
```
---
<h3> If you use this repository in your research, please cite the following paper: </h3>
  
```
bibtex
@article{Marquez_2023,
doi = {10.1088/1361-6528/acde83},
url = {https://dx.doi.org/10.1088/1361-6528/acde83},
year = {2023},
month = {jul},
publisher = {IOP Publishing},
volume = {34},
number = {39},
pages = {395201},
author = {Marquez, Bicky A and Singh, Jagmeet and Morison, Hugh and Guo, Zhimu and Chrostowski, Lukas and Shekhar, Sudip and Prucnal, Paul and Shastri, Bhavin J},
title = {Fully-integrated photonic tensor core for image convolutions},
journal = {Nanotechnology},
}
```

**This work can be use for convolutions, as the abstract of the cited article mentions:**

  Convolutions are one of the most critical signal and image processing operations. From spectral analysis to computer vision, convolutional filtering is often related to spatial information processing involving neighbourhood operations. As convolution operations are based around the product of two functions, vectors or matrices, dot products play a key role in the performance of such operations; for example, advanced image processing techniques require fast, dense matrix multiplications that typically take more than 90% of the computational capacity dedicated to solving convolutional neural networks. Silicon photonics has been demonstrated to be an ideal candidate to accelerate information processing involving parallel matrix multiplications. In this work, we experimentally demonstrate a multiwavelength approach with fully integrated modulators, tunable filters as microring resonator weight banks, and a balanced detector to perform matrix multiplications for image convolution operations. We develop a scattering matrix model that matches the experiment to simulate large-scale versions of these photonic systems with which we predict performance and physical constraints, including inter-channel cross-talk and bit resolution.

# PHYMRR


![MRR weightbank]([url_of_image](https://github.com/BickyMz/PHYMRR/blob/main/images/MRR_WB.png))

<h1> A Physical level simulation of a simple MRM and DEAP arrays </h1> 

<h3> The code implements variations of this circuit: </h3>

MRR/DEAP array illustration: ↓    
                                                                             Drop ->     ____
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
  
---

```bibtex
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

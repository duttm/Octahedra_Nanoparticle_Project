# Octahedra_Nanoparticle_Project


The purpose of this repo is two-fold:

(i). LD Simulations: To perform Langevin Dynamics (LD) simulations of anisotropic particles (in particular square and octahedral patchy particles) in order to mimic experimental self-assembly methods.

(ii). SymBOP Analysis: To analyze the assembly using novel techniques, including the Polyhedral Nematic Order Parameter and the Symmetrized Bond Order Parameter (SymBOP) to look for ordered domains.


LD Simulations:


SymBOP Analysis:

    This code is used to analyze the LD simulations discussed above. In particular, we want to locate regions of orientationally ordered domains in the final state of the simulations. The domains, in general, will possess bond-orientational order and polyhedral nematic order. The anisotropic nature of the building blocks used in the LD simulations (octahedral and square patchy particles) allows us to use a more sensitive characterization technique than the traditional bond-order parameters (BOPs). Our technique symmetrizes the BOPs (SymBOPs) and uses the underlying symmetry to characterize the local neighborhoods of each particle. In addition, the polyhedral nematic order parameter is used to quantify the relative orientations of the anisotropic particles themselves. Together, these order parameters allow us to pick out domains that contain specific bonding and orientational order. This particular code can only be used with anisotropic particles (currently only ideal octahedra and squares).



For more information see: 
- J. A. Logan,  S. Mushnoori,  M. Dutt, and A. V. Tkachenko, “Symmetry-specific orientational order parameters for complex structures,” (2021), arXiv:TBA [cond-mat.soft]
- S. Mushnoori, J. A. Logan, A. V. Tkachenko, and M. Dutt, “Controlling morphology in hybrid isotropic/patchy particle system,” (2021), arXiv:TBA [cond-mat.soft]
- The README documents in the corresponding folders.

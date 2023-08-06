 Virtual Observatory Model 
-----VERSION 01-----
%==========================================================================
Version numbering: 
->First two numbers relates to main field model: 01 uses versions of the CHAOS-6 model (e.g. CHAOS-6-x7)
->Second two numbers denotes different versions having same production time. 
%==========================================================================
Output files: The VOs are listed starting from the North pole by ascending time. 

VO_CHAMP_MF,VO_SWARM_MF  -> contains main field during CHAMP and Swarm periods. Format:  colatitude [deg], longitude [deg], Year, First of Month (March/July/November), Time [mjd], radius [km], B_r [nT], B_theta [nT], B_phi [nT], grad_r(Br) [nT/km], grad_theta(Btheta) [nT/km], grad_phi(Bphi) [nT/km], grad_theta(Br) [nT/km], grad_phi(Br) [nT/km], grad_theta(Bphi) [nT/km], No of data

VO_CHAMP_SV,VO_SWARM_SV -> contains secular variation during CHAMP and Swarm periods. Format:  colatitude [deg], longitude [deg], time [yrs], radius [km], dB_r [nT], dB_theta [nT], dB_phi [nT], grad_r(dBr/dt) [nT/km yr^⁻1], grad_theta(dBtheta/dt) [nT/km yr^⁻1], grad_phi(dBphi/dt) [nT/km yr^⁻1], grad_r(dBtheta/dt) [nT/km yr^⁻1], grad_r(dBphi/dt) [nT/km yr^⁻1],grad_theta(dBphi/dt) [nT/km yr^⁻1]

%==========================================================================
- VO data selection and correction:
    -CHAMP data, MAG-L3, from 2000-07-19 to 2010-09-17, 15 sec data sampling rate
    -Swarm data, Level 1b MAG-L version 0505, from 2013-11-29 to 2019-02-08, 15 sec data sampling rate
    -Gross outliers deviating more than 500nT from CHAOS-6-x8 removed  
    -Dark time (max 10deg above horizont)
    -Geomagnetically quiet conditions (kp<30,dDst<3,Em<0.8,Bz>0nT,abs(By)<10nT) 
    -Estimates of CHAOS-6-x8 main field (n=1-14) removed
    -Estimates of LCS-1 crustal field for SH degree n=15-185 (static part) removed 
    -Estimates of CHAOS-6-x8 magnetospheric and induced fields removed
    -Estimates of CIY4 ionopsheric and induced fields removed
%==========================================================================
- VO model setup
    -300 globally distributed VOs using an equal area grid (Leopardi 2006)
    -VO data search range is 700km around each VO location
    -VO data are collected for 4 months ad a time 
    -VO altitudes are 370km during CHAMP period
    -VO altitudes are 490km during Swarm period
    -Data along-track and cross-track(for Swarm only) differences and sums are used
    -VO fit using cubic potential description
    -Inversion limit = 30 data points
    -Data from Swarm A and C has been down weighted by a factor 1/2
    -For each epoch the CHAOS-6-x8 main field (n=1-14) prediction is added back.  
%==========================================================================
- Construction of the covariance matrices:
    -For MF/SV vector components the variances are constructed as described in Barrois etal. 2018 
    -For MF/SV gradients the variances are constructed from sigmas derived as the square root of the residuals std squared plus the residual mean squared, i.e. sigma=sqrt(sigma_mean^2+sigma_res^2)

-> Full matrices but they only contain the diagonal variance elements listed in the following order (thus there are not order consecutively by VO position):
 
1) For MF/SV vector components the diagonal elements are given for each component for all VOs like: [B_r(1,2,...,N); B_theta(1,2,...,N); B_phi(1,2,...,N)] where N is the number of VO 

2) For the MF/SV gradients the diagonal elements are given for each component for all VOs like: [rr(1,2,...,N); tt(1,2,...,N); pp(1,2,...,N); rt(1,2,...,N); rp(1,2,...,N); tp(1,2,...,N)]
%==========================================================================


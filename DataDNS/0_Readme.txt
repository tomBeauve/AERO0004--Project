%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%                                                           %%%%%%
%%%%%%                 Turbulent Round Jet Flow                  %%%%%%
%%%%%%                                                           %%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%                                                           %%%%%%
%%%%%%      Supported by the German Science Foundation (DFG)     %%%%%%
%%%%%%                                                           %%%%%%
%%%%%%            Project:    526024901                          %%%%%%
%%%%%%                                                           %%%%%%
%%%%%%                          and                              %%%%%%
%%%%%%                                                           %%%%%%
%%%%%%          Gauss Centre for Supercomputing e.V.             %%%%%%
%%%%%%                                                           %%%%%%
%%%%%%            Project:    pn73fu                             %%%%%%
%%%%%%                                                           %%%%%%
%%%%%%                          and                              %%%%%%
%%%%%%                                                           %%%%%%
%%%%%%          Studienstiftung des deutschen Volkes             %%%%%%
%%%%%%			  (Academic Scholarship Foundation)      %%%%%%
%%%%%%                                                           %%%%%%
%%%%%%                                                           %%%%%%
%%%%%%                                                           %%%%%%
%%%%%%                Chair of Fluid Dynamics                    %%%%%%
%%%%%%                                                           %%%%%%
%%%%%%         Department of Mechanical Engineering,             %%%%%%
%%%%%%            Technische Unversitaet Darmstadt,              %%%%%%
%%%%%%      Otto-Berndt-Str. 2, 64287 Darmstadt, Germany         %%%%%%
%%%%%%                                                           %%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%                                                           %%%%%%
%%%%%%                     <<< CAUTION >>>                       %%%%%%
%%%%%%                                                           %%%%%%
%%%%%%  All rights are reserved by the Chair of Fluid Dynamics.  %%%%%%
%%%%%%  No part of the data described herein may be represented  %%%%%%
%%%%%%  without reference. The data base may be used without     %%%%%%
%%%%%%  notification to the author's laboratory.                 %%%%%%
%%%%%%                                                           %%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%                                                                   %%
%%  NOMENCLATURE:                                                    %%
%%   r = radial coordinate                                           %%
%%   z = axial coordinate                                            %%
%%   phi = azimuthal coordinate                                      %%
%%   D = orifice diameter                                            %%
%%   U_i = mean velocity in direction i                              %%
%%   U_i U_j = mean of U_i U_j                                       %%
%%   u_b = bulk velocity at the orifice                              %%
%%                                                                   %%
%%   P = production                                                  %%
%%   D = dissipation                                                 %%
%%   T = turbulent transport                                         %%
%%   C = convection                                                  %%
%%   Pi = pressure-velocity-gradient tensor                          %%
%%   PT = pressure transport                                         %%
%%   PS = pressure strain                                            %%
%%                                                                   %%
%%   u_z = velocity in direction z                                   %%
%%   eta = r/z                                                       %%
%%   PDF = probability density function                              %%  
%%   PD = probability density                                        %%                                                 
%%   bin = bins normalized such that the sum of bin count is 1       %%
%%                                                                   %%
%%  NOTE:                                                            %%
%%   Reynold stress can be calculated with u_i u_j=U_i*U_j - U_i U_j %%
%%                                                                   %%
%%   "3_U_z_PDF.mat" contains "coord_U_z.mat" and "PDF.mat".         %% 
%%   Each row in "coord_U_z.mat" corresponds to                      %% 
%%   each cell entry of "PDF.mat"                                    %%
%%                                                                   %%
%%   coord_U_z.mat:                                                  %% 
%%     Each row is                                                   %% 
%%     [r, z, U_z(r=0,z)]                                            %%
%%                                                                   %%
%%   PDF.mat:                                                        %%
%%     Each cell entry is                                            %% 
%%     [bin, PD of u_z(eta,z,t)/U_z(r=0,z)]                          %% 
%%                                                                   %%
%%  BOX SIZE in D with axial length z=75: r(z=0)=2, r(z=75)=32       %%
%%  FLOW CONDITIONS:  Re_b = 3500,                                   %%
%%                     D=1, ubulk = 1                                %%
%%                                                                   %%
%%  Files:                                                           %%
%%   1_Moments.txt                                                   %%
%%   2_Turb_Budgets.txt                                              %%
%%   3_U_z_PDF.mat                                                   %%
%%                                                                   %%
%% Data files created: February 06, 2024                             %%
%%                                                                   %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
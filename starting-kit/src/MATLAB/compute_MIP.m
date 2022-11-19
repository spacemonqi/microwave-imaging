function [Vmax, kmax] = compute_MIP(V)
% COMPUTE_MIP Compute the maximum intensity projection (MIP) of a 3D volume.
%   [Vmax, kmax] = COMPUTE_MIP(V) computes the maximum intensity projection Vmax and the z-index 
%   corresponding to the estimated maximum.
%   
%   The z-index can be converted to a range using the z-vector zvec.

    % perform maximum intensity projection in z-direction
    [Vmax, kmax] = max(V,[],3);
end
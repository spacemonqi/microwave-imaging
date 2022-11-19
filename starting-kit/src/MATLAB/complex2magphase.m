function [mag, phi] = complex2magphase(V)
% COMPLEX2MAGPHASE Element-wise computation of the magnitude and the phase.
%   [mag, phi] = COMPLEX2MAGPHASE(V) Computes the magnitude mag and the phase phi for each element
%   im V.

    mag = abs(V);
    phi = angle(V);
end
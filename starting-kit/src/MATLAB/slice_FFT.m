function S = slice_FFT(im)
% SLICE_FFT Compute the 2D FFT of an image.
%   S = SLICE_FFT(im) Computes the 2D FFT of im.

    S = fftshift(fft2(im / numel(im)));
end
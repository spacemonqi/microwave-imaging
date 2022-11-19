[V, xvec, yvec, zvec] = import_volume('../../volumes/example-1.img');

Nx = numel(xvec);  % number of voxels in x-direction
Ny = numel(yvec);  % number of voxels in y-direction

c0 = 299792458;  % speed of light in m/s
lambda = c0 / 77e9;  % wavelength of the center frequency

kx_n = (-Nx/2:Nx/2-1) /((Nx-1)*diff(xvec(1:2))) * lambda;  % k-space vector in x-direction
ky_n = (-Ny/2:Ny/2-1) /((Ny-1)*diff(yvec(1:2))) * lambda;  % k-space vector in y-direction

% select z-slice to be visualized
zidx = 14;

[Vmax, kmax] = compute_MIP(V);
Vmax_range = abs([min(Vmax, [], 'all'), max(Vmax, [], 'all')]);
alpha_data = 1.8*(abs((Vmax - Vmax_range(1)) / (Vmax_range(2) - Vmax_range(1)))) - 0.25;

figure(1); clf('reset'); colormap('viridis');

% visualize magnitude of the MIP
subplot(231);
imagesc(xvec, yvec, 20*log10(abs(Vmax / max(Vmax, [], 'all'))), [-30 0]);
axis('image'); set(gca, 'YDir', 'normal');
title('Maximum intensity projection (MIP)');
cbar = colorbar(); xlabel(cbar, 'Normalized magnitude in dB')
xlabel('x in m'); ylabel('y in m');

% visualize phase of the MIP (opacity scaled by alpha_data)
[~, Vmax_phase] = complex2magphase(Vmax .* exp(1j*2*pi/lambda*2*zvec(kmax)));
h = subplot(232);
p = imagesc(xvec, yvec, 180/pi * Vmax_phase); axis('image'); set(gca, 'YDir', 'normal');
colormap(h, 'twilight');
set(p, 'AlphaData', alpha_data);
title('MIP Phase');
cbar = colorbar(); xlabel(cbar, 'Phase in degree');
xlabel('x in m'); ylabel('y in m');

% visualize the phase of a selected slice (opacity scaled by alpha_data)
[~, V_slice_phase] = complex2magphase(V(:,:,zidx));
h = subplot(233);
p = imagesc(xvec, yvec, 180 / pi * V_slice_phase); axis('image'); set(gca, 'YDir', 'normal');
colormap(h, 'twilight');
set(p, 'AlphaData', alpha_data);
title(sprintf('Single slice phase (z = %.4f m)', zvec(zidx)));
cbar = colorbar(); xlabel(cbar, 'Phase in degree');
xlabel('x in m'); ylabel('y in m');

% visualize the distance of the MIP (opacity scaled by alpha_data)
subplot(234);
p = imagesc(xvec, yvec, zvec(kmax)); axis('image'); set(gca, 'YDir', 'normal');
set(p, 'AlphaData', alpha_data);
colorbar();
title('MIP Distance');
cbar = colorbar(); xlabel(cbar, 'Distance in m');
caxis([0.15 0.28]);
xlabel('x in m'); ylabel('y in m');

% visualize the 2D FFT of the MIP
subplot(235)
S_MIP = slice_FFT(Vmax);
S_MIP_mag_dB = 20*log10(abs(S_MIP));
imagesc(kx_n, ky_n, S_MIP_mag_dB, max(S_MIP_mag_dB,[],'all')+[-35 0]);
hold('on'); plot(1*cos(linspace(0,2*pi,101)), 1*sin(linspace(0,2*pi,101)), 'w--'); hold('off');
axis('image');
set(gca, 'YDir', 'normal');
colorbar();
title('MIP 2D FFT');
xlabel('k_x in 2\pi / \lambda'); ylabel('k_y in 2\pi / \lambda');

% visualize the 2D FFT of a single slice
subplot(236)
S_slice = slice_FFT(V(:,:,zidx));
S_slice_mag_dB = 20*log10(abs(S_slice));
imagesc(kx_n, ky_n, S_slice_mag_dB, max(S_slice_mag_dB,[],'all')+[-35 0]);
hold('on'); plot(1*cos(linspace(0,2*pi,101)), 1*sin(linspace(0,2*pi,101)), 'w--'); hold('off');
axis('image');
set(gca, 'YDir', 'normal');
colorbar();
title(sprintf('Single slice 2D FFT (z = %.4f m)', zvec(zidx)));
set(gca,'GridColor',[1 1 1]);
xlabel('k_x in 2\pi / \lambda'); ylabel('k_y in 2\pi / \lambda');
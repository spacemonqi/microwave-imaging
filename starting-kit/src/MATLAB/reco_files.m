%% Create beamformer

%bf = SingleClusterBeamformer('CalDataDir', 'E:\measurements\QRAD\2022-09-27_Mirror\76000000000_81000000000_128\G1G2');
bf = SingleClusterBeamformer('CalDataDir', 'C:\Users\brinkm_m\Documents\Conferences\EuCAP 2023\measurements\71984251968_82023622047_256\G1G2');


%%
root_dir = 'C:\Users\brinkm_m\Documents\Git\qarsc.hackatum';

RAS_files = dir(fullfile(root_dir, 'measurements', '**', 'radar\N50random', '*.bin'));

% volume definition
xvec = linspace(-0.15, 0.15, 2^8+1);
yvec = linspace(-0.15, 0.15, 2^8+1);
zvec = 0.23 + linspace(-0.05, 0.05, 2^7+1);

figure(1); clf('reset');
%set(gcf, 'Position', [544          94        1111         898], 'Color', [1 1 1]);
set(gcf, 'Color', [1 1 1]);
colormap('viridis');

zidx = 40; % z-index when visualizing a single slice

for i = 1:numel(RAS_files)
    bf.load_measurement(fullfile(RAS_files(i).folder, RAS_files(i).name));
    bf.calibrate_measurement();
    
    V = bf.reco(xvec, yvec, zvec);

    [Vmax, kmax] = compute_MIP(V);
    alpha_data = 1.8*rescale(abs(Vmax)) - 0.25;
    
    % visualize magnitude of the MIP
    subplot(231);
    imagesc(xvec, yvec, 20*log10(abs(Vmax)), [-30 0]); axis('image'); set(gca, 'YDir', 'normal');
    title('Maximum intensity projection (MIP)');
    cbar = colorbar(); xlabel(cbar, 'Normalized magnitude in dB')
    
    % visualize phase of the MIP (opacity scaled by alpha_data)
    [~, Vmax_phase] = complex2magphase(Vmax .* exp(1j*2*pi/mean(bf.wav.lambda)*2*zvec(kmax)));
    h = subplot(232);
    p = imagesc(xvec, yvec, 180/pi * Vmax_phase); axis('image'); set(gca, 'YDir', 'normal');
    colormap(h, 'twilight');
    set(p, 'AlphaData', alpha_data);
    title('MIP Phase');
    cbar = colorbar(); xlabel(cbar, 'Phase in degree')
    
    % visualize the phase of a selected slice (opacity scaled by alpha_data)
    [~, V_slice_phase] = complex2magphase(V(:,:,zidx));
    h = subplot(233);
    p = imagesc(xvec, yvec, 180/pi * V_slice_phase); axis('image'); set(gca, 'YDir', 'normal');
    colormap(h, 'twilight');
    set(p, 'AlphaData', alpha_data);
    title(sprintf('Single slice phase (z = %.4f m)', zvec(zidx)));
    cbar = colorbar(); xlabel(cbar, 'Phase in degree')
    
    % visualize the distance of the MIP (opacity scaled by alpha_data)
    subplot(234);
    p = imagesc(xvec, yvec, zvec(kmax)); axis('image'); set(gca, 'YDir', 'normal');
    set(p, 'AlphaData', alpha_data);
    colorbar();
    title('MIP Distance');
    cbar = colorbar(); xlabel(cbar, 'Distance in m');
    caxis([0.15 0.28]);
    
    % visualize the 2D FFT of the MIP
    subplot(235)
    S_MIP = slice_FFT(Vmax);
    S_MIP_mag_dB = 20*log10(abs(S_MIP));
    imagesc(S_MIP_mag_dB, max(S_MIP_mag_dB,[],'all')+[-35 0]);
    axis('image');
    set(gca, 'YDir', 'normal');
    colorbar();
    title('MIP 2D FFT');
    
    % visualize the 2D FFT of a single slice
    subplot(236)
    S_slice = slice_FFT(V(:,:,zidx));
    S_slice_mag_dB = 20*log10(abs(S_slice));
    imagesc(S_slice_mag_dB, max(S_slice_mag_dB,[],'all')+[-35 0]);
    axis('image');
    set(gca, 'YDir', 'normal');
    colorbar();
    title(sprintf('Single slice 2D FFT (z = %.4f m)', zvec(zidx)));
    set(gca,'GridColor',[1 1 1])
    
    drawnow();
    f = getframe(gcf);
    [~, filename_without_ext, ~] = fileparts(fullfile(RAS_files(i).folder, RAS_files(i).name));
    
    % export the image
    export_dir_rel = strrep(RAS_files(i).folder, fullfile(root_dir, 'measurements'), 'export');
    if ~isfolder(fullfile(root_dir, export_dir_rel))
        mkdir(root_dir, export_dir_rel)
    end
    %imwrite(f.cdata, fullfile(root_dir, export_dir_rel, sprintf('%s.png', filename_without_ext)));
end
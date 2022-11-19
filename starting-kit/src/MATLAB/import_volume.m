function [V, xvec, yvec, zvec] = import_volume(filename_img)
% IMPORT_VOLUME Import 3D volume.
%   [V, xvec, yvec, zvec] = IMPORT_VOLUME(filename_img) Imports the 3D volume from filename_img and
%   returns the volume definition given as the coordinate vectors in x-, y-, and z-direction.

    [filepath, filename_tmp] = fileparts(filename_img);
    filename_header = fullfile(filepath, sprintf('%s.hdr', filename_tmp));

    if ~exist(filename_img, 'file')
        error("File '%s' does not exist.", filename);
    end

    if ~exist(filename_header, 'file')
        error("Header file '%s' does not exist.", filename_header);
    end

    V_tmp = niftiread(filename_header, filename_img);

    N = size(V_tmp, 3);

    V = V_tmp(:,:,1:N/2) .* exp(1j * V_tmp(:,:,N/2+1:N));
    
    def = jsondecode(fileread(fullfile(filepath, sprintf('%s.json', filename_tmp))));
    xvec = def.origin.x + (0:def.dimensions.x-1) * def.spacing.x;
    yvec = def.origin.y + (0:def.dimensions.y-1) * def.spacing.y;
    zvec = def.origin.z + (0:def.dimensions.z-1) * def.spacing.z;
end
% Power Spectrum Ananlysis of a Image
%
% Usage:
%   [freq, power] = powerspectrum(filename, resolution, Dtheta);
%   [freq, power] = powerspectrum(filename, resolution, start_theta, Dtheta, end_theta);
%
% Units:
%   resolution: meter
%   Dtheta: radian
%
% Examples:
%  1) resolution = 9 nm, Dtheta = 0.01
%   [freq, power] = powerspectrum('Siemens_1st.tiff', 9*10^-9, 0.01);
%  2) resolution = 9 nm, start_theta = pi/8, Dtheta = 0.01, end_theta = pi
%   [freq, power] = powerspectrum('Siemens_1st.tiff', 9*10^-9, pi/8, 0.01, pi);
%
% References:
%   Chen, T. Y., et al. (2011). Optics Express, 19(21), 19919-19924.
%
% Contact:
%   Hyounggyu Kim (khg@gist.ac.kr)

function [freq, power] = powerspectrum(filename, resolution, varargin)

    % Read image and fourier transform
    imdata = imread(filename);
    imdata = double(imdata) / double(max(imdata(:))); % Nomalize 0~1
    imdata = fftshift(fft2(imdata));
    imdata = imdata.*conj(imdata);

    % Set constants
    [imheight, imwidth] = size(imdata);

    % Calculate Spatial Frequency
    max_freq = 1/(2*resolution);
    freq = linspace(0, max_freq, imwidth/2-1);
    
    nVarargs = length(varargin);
    if nVarargs == 1
        theta = 0:varargin{1}:2*pi;
    elseif nVarargs == 3
        theta = varargin{1}:varargin{2}:varargin{3};
    end
    % start_theta <= theta < end_theta
    theta = theta(1:end-1);
    
    % Calculate Power
    radius = min(imwidth, imheight);
    power = arrayfun(@(r) integral(r), 1:radius/2-1);
    function ret_val = integral(r)
        x = round(r*cos(theta))+imwidth/2;
        y = round(r*sin(theta))+imheight/2;
        idx = sub2ind([imheight, imwidth], y, x);
        ret_val = sum(imdata(idx));
    end

end
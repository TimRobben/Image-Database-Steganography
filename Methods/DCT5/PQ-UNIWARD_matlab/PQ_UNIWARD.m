function [S_STRUCT, pChangeP1, pChangeM1] = PQ_UNIWARD(precoverPath, coverPath, stegoPath, payload, QF2)
% -------------------------------------------------------------------------
% PQ_UNIWARD grayscale Embedding    |   November 2020   |      version 1.0 
% -------------------------------------------------------------------------
% INPUT:
%  - precoverPath ... Path to the grayscale JPEG compressed precover image.
%  - coverPath ... Path to which store the double compressed cover image.
%  - stegoPath ... Path to which store the double compressed stego image.
%  - payload ... Embedding payload in bits per non-zero AC DCT coefficients
%              (bpnzac).
%  - QF2 ... Quality factor for the second compression.
% OUTPUT:
%  - S_STRUCT ... Resulting JPEG structure with embedded payload.
%  - pChangeP1 ... Embedding change probabilities by +1. 
%  - pChangeM1 ... Embedding change probabilities by -1. 
% -------------------------------------------------------------------------
% Copyright (c) 2020 DDE Lab, Binghamton University, NY.
% All Rights Reserved.
% -------------------------------------------------------------------------
% Permission to use, copy, modify, and distribute this software for
% educational, research and non-profit purposes, without fee, and without a
% written agreement is hereby granted, provided that this copyright notice
% appears in all copies. The program is supplied "as is," without any
% accompanying services from DDE Lab. DDE Lab does not warrant the
% operation of the program will be uninterrupted or error-free. The
% end-user understands that the program was developed for research purposes
% and is advised not to rely exclusively on the program for any reason. In
% no event shall Binghamton University or DDE Lab be liable to any party
% for direct, indirect, special, incidental, or consequential damages,
% including lost profits, arising out of the use of this software. DDE Lab
% disclaims any warranties, and has no obligations to provide maintenance,
% support, updates, enhancements or modifications.
% -------------------------------------------------------------------------
% Contact: jbutora1@binghamton.edu
%          November 2020
%          http://dde.binghamton.edu/download/
% -------------------------------------------------------------------------
% References:
% [1] - J. Butora and J. Fridrich. Revisiting Perturbed quantization.
%       9th IH&MMSec. Workshop
% -------------------------------------------------------------------------

precover = jpeg_read(precoverPath);
nzAC = nnz(precover.coef_arrays{1}) - ...
    nnz(precover.coef_arrays{1}(1:8:end,1:8:end)); % number of nonzero AC DCT coefficients

PC_SPATIAL = double(imread(precoverPath));
C_STRUCT = precover;
C_QUANT = Qmatrix(QF2);
C_STRUCT.quant_tables{1} = C_QUANT;

fun=@(x) dct2(x.data);
xi= blockproc(double(PC_SPATIAL)-128,[8 8],fun);

% Quantization
fun = @(x) x.data./C_QUANT;
DCT_real = blockproc(xi,[8 8],fun);
DCT_rounded = round(DCT_real);

C_STRUCT.coef_arrays{1} = DCT_rounded;

e = DCT_real - DCT_rounded;             % Compute rounding error
direction = sign(e);
%%-------------------------------
%%      BEGIN costs
%%-------------------------------

wetConst = 10^13;
sgm = 2^(-6);

%% Get 2D wavelet filters - Daubechies 8
% 1D high pass decomposition filter
hpdf = [-0.0544158422, 0.3128715909, -0.6756307363, 0.5853546837, 0.0158291053, -0.2840155430, -0.0004724846, 0.1287474266, 0.0173693010, -0.0440882539, ...
        -0.0139810279, 0.0087460940, 0.0048703530, -0.0003917404, -0.0006754494, -0.0001174768];
% 1D low pass decomposition filter
lpdf = (-1).^(0:numel(hpdf)-1).*fliplr(hpdf);

F{1} = lpdf'*hpdf;
F{2} = hpdf'*lpdf;
F{3} = hpdf'*hpdf;

%% Pre-compute impact in spatial domain when a jpeg coefficient is changed
spatialImpact = cell(8, 8);
for bcoord_i=1:8
    for bcoord_j=1:8
        testCoeffs = zeros(8, 8);
        testCoeffs(bcoord_i, bcoord_j) = 1;
        spatialImpact{bcoord_i, bcoord_j} = idct2(testCoeffs)*C_QUANT(bcoord_i, bcoord_j);
    end
end

%% Pre compute impact on wavelet coefficients when a jpeg coefficient is changed
waveletImpact = cell(numel(F), 8, 8);
for Findex = 1:numel(F)
    for bcoord_i=1:8
        for bcoord_j=1:8
            waveletImpact{Findex, bcoord_i, bcoord_j} = imfilter(spatialImpact{bcoord_i, bcoord_j}, F{Findex}, 'full');
        end
    end
end

%% Create reference cover wavelet coefficients (LH, HL, HH)

% precover
padSize = max([size(F{1})'; size(F{2})']);
PC_SPATIAL_PADDED = padarray(PC_SPATIAL, [padSize padSize], 'symmetric'); % pad image

R_PC = cell(size(F));
for i=1:numel(F)
    R_PC{i} = imfilter(PC_SPATIAL_PADDED, F{i});
end

[k, l] = size(PC_SPATIAL);

rho = zeros(k, l);
tempXi = cell(3, 1);
%% Computation of costs
for row = 1:k
    for col = 1:l
        modRow = mod(row-1, 8)+1;
        modCol = mod(col-1, 8)+1;        
        
        subRows = row-modRow-6+padSize:row-modRow+16+padSize;
        subCols = col-modCol-6+padSize:col-modCol+16+padSize;
     
        for fIndex = 1:3
            % compute residual
            R_PC_sub = R_PC{fIndex}(subRows, subCols);
            % get differences between precover and cover, stego
            wavCoverStegoDiff = waveletImpact{fIndex, modRow, modCol};
            % compute suitability
            
            tempXi{fIndex} = abs(wavCoverStegoDiff)./ (abs(R_PC_sub)+sgm);
        end
        rho_temp = tempXi{1} + tempXi{2} + tempXi{3};
        rho(row, col) = sum(rho_temp(:));
    end
end

% rho = rho + 10^(-4);
rho(rho > wetConst) = wetConst;
rho(isnan(rho)) = wetConst;    

% Avoid 04 coefficients with e on boundaries: e=+-1/2
maxCostMat = false(size(rho));
maxCostMat(1:8:end, 1:8:end) = true;
maxCostMat(5:8:end, 1:8:end) = true;
maxCostMat(1:8:end, 5:8:end) = true;
maxCostMat(5:8:end, 5:8:end) = true;

g = C_QUANT./gcd(C_QUANT, precover.quant_tables{1});
contrib_ind = 2*((mod(g,2)==0) | (g==1))-1;
fun_cont = @(x) x.data .* contrib_ind;
rho = blockproc(rho, [8, 8], fun_cont);
rho(rho<0) = wetConst;

rhoP1 = rho;
rhoM1 = rho;
weighted_rho = (1-2.*abs(e)) .* rho;
rhoP1(direction == 1) = weighted_rho(direction == 1);
rhoM1(direction == -1) = weighted_rho(direction == -1);


rhoP1(DCT_real>1022) = wetConst;
rhoM1(DCT_real<-1022) = wetConst;
rhoP1(maxCostMat & (abs(e)>0.4999)) = wetConst;
rhoM1(maxCostMat & (abs(e)>0.4999)) = wetConst;

%% Embedding simulation
[S_COEFFS, pChangeP1, pChangeM1] = EmbeddingSimulator(DCT_rounded, rhoP1, rhoM1, round(payload * nzAC));

S_STRUCT = C_STRUCT;
S_STRUCT.coef_arrays{1} = S_COEFFS;

% Save cover
if ~exist(coverPath, 'file')
    jpeg_write(C_STRUCT, coverPath);
end

% Save stego
if ~exist(stegoPath, 'file')
    jpeg_write(S_STRUCT, stegoPath);
end

function [y, pChangeP1, pChangeM1] = EmbeddingSimulator(x, rhoP1, rhoM1, m)

    x = double(x);
    n = numel(x);
    
    lambda = calc_lambda(rhoP1, rhoM1, m, n);
    pChangeP1 = (exp(-lambda .* rhoP1))./(1 + exp(-lambda .* rhoP1) + exp(-lambda .* rhoM1));
    pChangeM1 = (exp(-lambda .* rhoM1))./(1 + exp(-lambda .* rhoP1) + exp(-lambda .* rhoM1));

    randChange = rand(size(x));
    y = x;
    y(randChange < pChangeP1) = y(randChange < pChangeP1) + 1;
    y(randChange >= pChangeP1 & randChange < pChangeP1+pChangeM1) = y(randChange >= pChangeP1 & randChange < pChangeP1+pChangeM1) - 1;
    
    function lambda = calc_lambda(rhoP1, rhoM1, message_length, n)

        l3 = 1e3;
        m3 = double(message_length + 1);
        iterations = 0;
        while m3 > message_length
            l3 = l3 * 2;
            pP1 = (exp(-l3 .* rhoP1))./(1 + exp(-l3 .* rhoP1) + exp(-l3 .* rhoM1));
            pM1 = (exp(-l3 .* rhoM1))./(1 + exp(-l3 .* rhoP1) + exp(-l3 .* rhoM1));
            m3 = ternary_entropyf(pP1, pM1);
            iterations = iterations + 1;
            if (iterations > 10)
                lambda = l3;
                return;
            end
        end        
        
        l1 = 0; 
        m1 = double(n);        
        lambda = 0;
        
        alpha = double(message_length)/n;
        % limit search to 50 iterations
        % and require that relative payload embedded is roughly within 1/1000 of the required relative payload        
        while  (double(m1-m3)/n > alpha/1000.0 ) && (iterations<50)
            lambda = l1+(l3-l1)/2; 
            pP1 = (exp(-lambda .* rhoP1))./(1 + exp(-lambda .* rhoP1) + exp(-lambda .* rhoM1));
            pM1 = (exp(-lambda .* rhoM1))./(1 + exp(-lambda .* rhoP1) + exp(-lambda .* rhoM1));
            m2 = ternary_entropyf(pP1, pM1);
    		if m2 < message_length
    			l3 = lambda;
    			m3 = m2;
            else
    			l1 = lambda;
    			m1 = m2;
            end
    		iterations = iterations + 1;
        end
    end
    
    function Ht = ternary_entropyf(pP1, pM1)
        pP1 = pP1(:);
        pM1 = pM1(:);
        Ht = -(pP1.*log2(pP1))-(pM1.*log2(pM1))-((1-pP1-pM1).*log2(1-pP1-pM1));
        Ht(isnan(Ht)) = 0;
        Ht = sum(Ht);
    end

end

end

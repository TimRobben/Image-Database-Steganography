function Q=Qmatrix_chrominance(quality)
% Q=Qmatrix(quality)
% JPEG quantization matrix for 8x8 dct block as a function of the quality factor
% quality   should be an integer between 1 and 100 (default is 50)

if nargin<1, quality=50; end
Q50=[17 18 24 47  99  99  99  99
     18 21 26 66  99  99  99  99
     24 26 56 99  99  99  99  99
     47 66 99 99  99  99  99  99
     99 99 99 99  99  99  99  99
     99 99 99 99  99  99  99  99
     99 99 99 99  99  99  99  99
     99 99 99 99  99  99  99  99];  % Quantization matrix for 50% quality
  
if quality>=50, 
   Q=max(1,round(2*Q50*(1-quality/100)));
   %Q = 2*Q50*(1-min(quality,99.9)/100);
else  
   Q=min(255,round(Q50*50/quality)); 
end

A = imread("E:\Scriptie\Methods\SampleDB\XIAOMI Poco F3 - HDR\IMG_20210517_230713.JPG");
REF = imread("E:\Scriptie\Methods\data\jpg\XIAOMI Poco F3 - HDR\IMG_20210517_230713.JPG");
peakpsnr = psnr(A, REF);


fprintf('\n The Peak-SNR value is %0.4f', peakpsnr);
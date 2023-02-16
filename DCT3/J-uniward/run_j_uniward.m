function run_script = runjuniward(Cover, Stego, Alpha)
addpath('jpeg_toolbox');
jpeg_write(J_UNIWARD(Cover, Alpha), Stego)
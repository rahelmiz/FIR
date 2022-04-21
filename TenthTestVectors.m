% test vectors for Tenth filter (decimation by 10 eventually)12-19-2021KLT

load('Tenth.mat')  % the coefficients stored here from filterDesigner, Num
% they are quantized to a fractional signed 16 bit number, so we have to
% multiply by 2^15 to get the integer value for simulation
b = Num * 2^15 * 8;  % huh...had to multiply by 8 to match *.coe file
% assume something wrong with coe coefficients; 8x too big
% figure;plot(b);grid on;title('Tenth filter coefficients');
%
numCoeff = length(b);  % how many coefficients?

% generate integer test vectors, assuming 16 bit input width.  Pick the
% length so it will fit in an FPGA block ram, potentially as a test vector
% location, and pick frequencies such that the memory can wrap...that is,
% loop over and over without phase jumps in the signal
% assume block length of 16 bits by 1024 samples.  multiples of Fs/1024 fit
Fs = 100.0;
F1 = Fs/1024*41;  % in passband, at edge  4.004
F2 = Fs/1024*51;  % close to alias point  4.980
F3 = Fs/1024*65;  % in stop-band   6.35
a1 = 1.0;  % amplitudes for checking ...
a2 = 1.0;
a3 = 1.0;

t = 1:1026;  % time increment.  generate 2 more samples to verify they match
% stagger phases of the sine waves to reduce peak to average
sig = a1*cos(t*F1/Fs*2*pi) + a2*sin(t*F2/Fs*2*pi) + a3*cos(t*F3/Fs*2*pi+0.8);  
% make full scale signed integer values
sigi = round(sig/max(abs(sig))*(2^15 - 1));
max(sigi)
min(sigi)  % check max values of 32767
% figure;plot(sigi);grid on;title('Test Vector Input');
% an alternate test vector is random noise.  Random numbers span the entire
% spectrum, and are sometimes useful to verify spectral response in a
% monte-carlo approach.  It takes a LOT of samples to get a low variance
% response though, so VHDL simulation typically won't do this.

% now we simulate the filter.  This can become quite sophisitcated, but in
% this case we will brute force the calculations, in matlab double float
% precision.  That carries 48 bits of resolution.  Our 16 x 16 multiply
% will generate 31 bit outputs, so we can sum 17 more bits worth of samples
% 2^17 = 128K samples, and our filter is smaller than that, so we don't
% have to worry about precision and overflow

% this filter implementation assumes we will have a numCoeff input signal
% shift register, preloaded with zeros.  The first input sample will be
% multiplied by the first coefficent to generate the first output sample.
% The second output sample is the sum of the first input sample times the
% second coefficient, plus the second input sample times the first
% coefficient, and so on.  We could add zeros to the test vector to 'flush'
% the filter (or loop the input), but for simulation we already have fully loaded the filter,
% so it isn't necessary.

delays = zeros(1,numCoeff);  % delay line, initialized to zero
fout = zeros(1,length(sigi));  % simulation output
accout = fout;  % full precision accumulator

for i = 1:length(sigi)  % iterate through the input test vector
    % shift in signal
    for k = numCoeff:-1:2  % counting index down
        delays(k) = delays(k-1); % shift the delays
    end
    delays(1) = sigi(i);
    % calculate filter output
    accum = 0;
    for j = 1:numCoeff
        accum = accum + delays(j)*b(j);  % we could do this quickly with matlab vector notation, but this way for clarity
    end
    %  now we have a high precision accumulator, but only 16 bits out.  We
    %  can either round or truncate, depending on the implementation
    %  options.  Rounding is nicer mathematically, and if you are doing
    %  long integrations (no dc bias offset accumulation), but truncation
    %  is simpler
    fout(i) = floor(accum/32768/8);  % divide by 32768 to get to 16 bits  divide by 8 for scaled coe coefficients
    accout(i) = accum;  % for debug, accumulator sums
end

figure;plot(sigi);grid on;hold on;plot(fout,'g');title('in and out');
% note that group delay of the filter is half the length

% print out the test vector files
fp = fopen('TenthInput.txt','w');
fp2 = fopen('TenthAccum.txt','w');
fp3 = fopen('TenthOut.txt','w');

for i = 1:length(fout)
    fprintf(fp,'%d\n',sigi(i));
    fprintf(fp2,'%d\n',accout(i));
    fprintf(fp3,'%d\n',fout(i));
end
fclose(fp);
fclose(fp2);
fclose(fp3);


function [fshift,powershift] = fft_analysis(data, Fs)
    fft_ = fft(data);
    n=length(data);
    Y = fftshift(fft_);
    fshift = (-n/2:n/2-1)*(Fs/n);
    powershift = abs(Y).^2;    
end

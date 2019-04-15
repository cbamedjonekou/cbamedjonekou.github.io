% Run 1

Fs = 100;
t = (0:99)/Fs;
A = 2;
w0 = 2*pi*1;
s = (sin(w0*t));
for n = 3:2:30
    s = s+1/n*sin(n*w0*t);
end
s = A/2 + (2*A)/pi*s;
subplot(2, 2, 1)
plot(t,s),grid
xlabel('Time in seconds')
ylabel('Amplitude')
title('Square Wave')

% Run 2

m = 3;
Rp = 0.1;
Rs = 40;
Wn = 0.8;
[b, a] = ellip(m,Rp,Rs,Wn);
[H,w] = freqz(b,a);
subplot(2, 2, 2)
plot(w*Fs/(2*pi),abs(H)),grid
xlabel('Frequency in Hz');
ylabel('Amplitude')
title('Low Pass Filter')

% Run 3 Part 1

sf = filter(b,a,s);
subplot(2, 2, 3)
plot(t,sf)
xlabel('Time in seconds');
ylabel('Amplitude')
title('Filtering in the Time Domain')

% Run 3 Part 2
S = fft(s, 512);
SF = fft(sf, 512);
f = (0:255)/256*(Fs/2);
subplot(2, 2, 4)
vari = abs([S(1:256);SF(1:256);]);
plot(f, vari), grid
xlabel('Frequency in Hz');
ylabel('Amplitude')
title('Filtering in the Frequency Domain')


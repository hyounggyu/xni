% Usage:
%  loglogplot(freq, power, 10, 1000)

function loglogplot(freq, power, min_r, max_r)
  loglog(freq(min_r:max_r)/10^6, power(min_r:max_r)); % '10^6' => 1/um
  set(gca, 'XTick', [0.1 0.2 0.4 0.6 1 2 4 6 8 10 20 40 60 ]);
  xlabel('Spatial Frequency [ 1/um ]')
  ylabel('Power (Arbitary Units)')
end
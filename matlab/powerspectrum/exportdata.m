% Usage:
%  exportdata('powerspecdata.txt', freq, power)

function exportdata(filename, freq, power)
  powerspecdata = transpose([freq; power]);
  save(filename, 'powerspecdata', '-ascii');
end
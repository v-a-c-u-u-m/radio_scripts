# Radio Scripts



## Dependencies
GNU Radio Companion 3.7.10



## Usage
### Receiving and recording ELF/VLF example
```sh
gnuradio-companion elf_vlf.grc
```



### Interval coding
Generating a file with pulse spacing in hertz
as example, 8 Hz, 8 Hz, 10 Hz, 10 Hz
```sh
printf "\x08\x08\x10\x10" > byte.bin
```

or in double format
as example, 9.8 Hz, 10 Hz, 7.83 Hz
```sh
python3 -c 'from struct import pack; f=open("double.bin", "wb"); f.write(pack("d", 9.80) + pack("d", 10) + pack("d", 7.83))'
```

Encode data into wav file, where
f - carrier frequency, s - sample rate, c - number of pulsations at the carrier frequency, r - read format
```sh
./interval_coding.py double.bin -f 501 -s 80000 -c 32 -t 1 -r double
./interval_coding.py byte.bin -f 501 -s 80000 -c 4 -t 1 -r byte
```

Using frequencies from keyboard input
```sh
./interval_coding.py "7.83 10 7.83 10" -f 501 -s 80000 -c 23 -t 1
```

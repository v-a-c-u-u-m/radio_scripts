# Radio Scripts



## Dependencies
GNU Radio Companion 3.7.10



## Usage
Receiving and recording ELF/VLF example
```sh
gnuradio-companion elf_vlf.grc
```

Interval coding
```sh
./interval_coding.py double.bin -f 501 -s 80000 -c 32 -t 1 -r double
./interval_coding.py byte.bin -f 501 -s 80000 -c 4 -t 1 -r byte
```

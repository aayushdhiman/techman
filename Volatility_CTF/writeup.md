The first thing given to us on the .onion link was a .raw file titled "memory dump."

Using Volatility, we were able to access the contents of the .raw file given, showing us the actual contents of the memory dump and the processes that were running at the time fo the dump.

After searching for mutexes within the memory dump, a base64 string was found. When decoded, this produced a hexadecimal string. When decoded to ascii a second time, this produced the key: KEY{3 2 8 6 4 7 7 3}.

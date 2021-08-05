The Beginning:

The first item given to us on the .onion link for this challenge was a .raw file titled "memory dump."

Interaction with Volatility:

Using Volatility within CarsonOS, we were able to access the contents of the .raw file given, showing us the actual contents of the memory dump and the processes that were running at the time of the dump.

First attempt with the Memory Dump:

Originally, we were loooking through the dump to find processes that looked out of place or suspicious, but we kept hitting dead ends. However, eventually we found a compelling article online about mutexes and how they are paired with memory dumps.

Finale:

Eventually, after searching for mutexes within the memory dump, a base64 string was found. When this string was decoded, a hexadecimal string was produced. When decoded to ascii a second time, this produced the key to the challenge: KEY{3 2 8 6 4 7 7 3}.


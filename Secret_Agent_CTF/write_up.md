# Getting the file

---

After playing through the game, the file was retrieved from [this onion link]([http://f4nmfiwcj7v6e6oisd6znce3d7hm6ducuq7qmkaeu3k7oa6dqn237nad.onion](http://f4nmfiwcj7v6e6oisd6znce3d7hm6ducuq7qmkaeu3k7oa6dqn237nad.onion/)). The files were downloaded from the image for The Musician and The Nerd. 

# The Child

---

The first flag was very simple, it was contained in the QR code that was on the image.

CF{babyyoda}

# The First Dump

---

This flag was contained in the hexdump of the agent.png file. You can either run strings on the file and you'll see the flag, or you can xxd the image and you'll see it at the end.

CF{h3xDuMp_FTW}

# Stegosaurus Hex

---

This was just getting the stegged message out of the image, which was fairly simple considering that the .txt file told me that the image was stegged. I built a Python script using PIL and bitstring to pull the least significant bit from the image's RGBA channels. The script is attached to the GitHub repo. In the hex from pulling the least significant bit, there was a message to the next part of the challenge and the flag.

CF{steg_totally_rocks}

# The Moonwalk

---

The hint that I got out of the least significant bit output told me that the binary that was above it was encrypted with DES (single DES). I tossed it through the DES decryption on CyberChef and used the first flag (babyyoda) as the key. The output gave me the zip file (phase4.zip).

CF{luk3_b1nw4lk3r}

# The Avengers

---

This flag was in the assembly for crackme in the zip file. Once decompiled, there was a stringcompare that included a comparison between s and CF{%s_%s_%s}, vision, hearts, wanda. The purpose of the line is to compare s, the user input, with V1s10n (vision), h34RTs (hearts), and W4nd4 in the format of CF{V1s10n_h34RTs_W4nd4}.

 

# The Real Flag

---

The final flag was given to us after inputting the correct password. 

flag{8 3 4 0 3 2 7 3}

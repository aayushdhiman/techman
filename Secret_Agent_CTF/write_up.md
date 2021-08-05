# The Child

---

The first flag was very simple, it was contained in the QR code that was on the image.

CF{babyyoda}

# The First Dump

---

This flag was contained in the hexdump of the agent.png file. I ran the strings command on agent.pngt to see the flag at the end of the file. Alternatively, one could run the xxd command on agent.png and see it at the end of the hexdump.

CF{h3xDuMp_FTW}

# Stegosaurus Hex

---

The readme of this phase let me know that the image was stegged. It included an explanation of what Least Significant Bit steganography is and described how to crack it. I wrote a python script (attached) that would extract the last bit of each channel of each pixel. I found the stegged flag, as well as instructions for the next flag. 

<details>
  <summary>LSB Code</summary>
    
    from PIL import Image
    import bitstring

    img = 'C:\\Users\\student\\Desktop\\agent.png'

    extracted_bin = []
    with Image.open("C:\\Users\\student\\Desktop\\agent.png") as img:
        width, height = img.size
        for x in range(0, width):
            for y in range(0, height):
                pixel = list(img.getpixel((x, y)))
                for n in range(0,4):
                    extracted_bin.append(pixel[n]&1)
                    # print(pixel[n]&1)

    data = "".join([str(x) for x in extracted_bin])

    output = open("output.bin", "wb+")
    output.write((bitstring.BitArray(bin=data)).tobytes())
  
</details>

CF{steg_totally_rocks!}

# The Moonwalk

---

The hint that I got out of the least significant bit output told me that the binary that was above it was encrypted with DES (single DES). I tossed it through the DES decryption on CyberChef and used the first flag (babyyoda) as the key. The output gave me the zip file (phase4.zip). The flag for this phase was contained in the least significant bit output, after the binary. 

CF{luk3_b1nw4lk3r}

# The Avengers

---

This flag was in the assembly for crackme in the zip file. Once decompiled, there was a stringcompare that included a comparison between s and CF{%s_%s_%s}, vision, hearts, wanda. The purpose of the line is to compare s, the user input, with V1s10n (vision), h34RTs (hearts), and W4nd4.

CF{V1s10n_h34RTs_W4nd4}

# The Real Flag

---

The final flag was given to us after inputting the correct password. 

flag{8 3 4 0 3 2 7 3}

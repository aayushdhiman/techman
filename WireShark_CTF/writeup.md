Provided was a readme file, a pdf file documenting the communication and encryption process, and a pcap file containing the encrypted packets.

The first step was to examine the documentation and determine how the client and the AP communicate and authenticate.

<details>
  <summary>Simplified Documentation</summary>
  
### Connection:
1. The AP sends a beacon every three seconds containing its SSID
2. The client responds with a probe request containing the AP's SSID and the string "H4ck02Auth".
3. The AP replies with a probe response containing its SSID and the authorization magic.

---

### Authentication:
1. The client sends an authentication frame
2. The AP sends the first key (K1) containing a random 4 byte HMAC (`AP_HMAC`) and the router password. Both are XOR'd using the authorization magic.
3. The client decodes the key using the authorization magic, then sends a second key (K2) containing a random 4 byte HMAC (`Client_HMAC`) and the router password. Both are XOR'd using the AP_HMAC
4. The AP sends a K3 verifying whether the authentication was successful or not.

---

### Encryption:
1. The plaintext message is encrypted using AES. The encryption key is the MD5 hash of the `Client_HMAC` appended to the `AP_HMAC` (`Client_HMAC + AP_HMAC`).
2. The ciphertext is split into blocks of 255 bytes or less.
3. Each block is encoded using base64.

---

### Transmission:
1. Each block is sent as an individual packet from the client to the AP. Each packet contains the total size of the message directly before the block.
2. The AP decodes and collects each block until the total size is reached, then decrypts the ciphertext into the original message.
  
---
  
</details>

## Reversing the encryption:
#### 1. Open the `extracted-wireless-recon.pcapng` file in Wireshark.
#### 2. Retrieve the authentication magic from the last four bytes of the probe response (packet 18):
   - <details>
     <summary>Authentication Magic</summary>
     <pre>48 4b 0a 0b</pre>
     </details>
   
#### 3. Retrieve the encrypted `AP_HMAC` and router password from the last 16 bytes of the K1 association request (packet 24):
   - <details>
     <summary>Encrypted <code>AP_HMAC</code> and router password</summary>
     <pre>98 56 e3 9a 3b 3e 7a 6e 3a 38 6f 68 3a 2e 7e 2a</pre>
     </details>
   
#### 4. Decrypt the `AP_HMAC` and the router password by XORing them in <a href=https://www.dcode.fr/xor-cipher>Dcode</a> using the authentication magic as the key:
   - <details>
     <summary>Decrypted <code>AP_HMAC</code> and router password</summary>
     <pre>
        98 56 e3 9a 3b 3e 7a 6e 3a 38 6f 68 3a 2e 7e 2a
     ⊕ 48 4b 0a 0b|-----------|-----------|---------->
     =  d0 1d e9 91 73 75 70 65 72 73 65 63 72 65 74 21
     </pre>
     This contains two sections:
        <ul>
          <li>The <code>AP_HMAC</code>: <code>d0 1d e9 91</code></li>
          <li>The router password: <code>73 75 70 65 72 73 65 63 72 65 74 21</code> which reads <code>supersecret!</code> in ascii</li>
        </ul>
     </details>
   
#### 5. Retrieve the encrypted `Client_HMAC` and router password from the last 16 bytes of the K2 association request (packet 25):
   - <details>
     <summary>Encrypted <code>Client_HMAC</code> and router password</summary>
     <pre>3e 03 ff c1 a3 68 99 f4 a2 6e 8c f2 a2 78 9d b0</pre>
     </details>
   
#### 6. Decrypt the `Client_HMAC` and router password by XORing them in <a href=https://www.dcode.fr/xor-cipher>Dcode</a> using the `AP_HMAC` as the key.
   - <details>
     <summary>Decrypted <code>Client_HMAC</code> and router password</summary>
     <pre>
        3e 03 ff c1 a3 68 99 f4 a2 6e 8c f2 a2 78 9d b0
     ⊕ d0 1d e9 91|-----------|-----------|---------->
     =  ee 1e 16 50 73 75 70 65 72 73 65 63 72 65 74 21
     </pre>
     The router password is already known, so only the first four bytes are relevant, as this is the <code>Client_HMAC</code>:
        <ul>
        <li><pre>ee 1e 16 50</pre></li>
        </ul>
     </details>
   
#### 7. Find the MD5 hash value of `Client_HMAC + AP_HMAC` using <a href=https://cryptii.com/pipes/md5-hash>Cryptii</a> to determine the encryption key.
   - <details>
     <summary>MD5 hash of <code>Client_HMAC + AP_HMAC</code></summary>
     <pre>
     md5(d0 1d e9 91 ee 1e 16 50) = 8b 25 ab 2c 0d 32 6b ba e2 79 07 65 54 39 7f 64
     </pre>
     </details>
   
#### 8. Collect each block of the ciphertext (the last 340 bytes) from the last five packets (packets 27-31). The final block (packet 32) only consists of 180 bytes, rather than 340:
   - <details>
     <summary>Encoded blocks</summary>
     <pre>
     56 34 57 50 74 38 72 2f 55 63 31 34 47 70 6b 73 79 72 32 69 34 6c 59 61 75 42 36 6b 61 34 63 5a 33 71 75 6e 75 59 4a 7a 59 66 64 4e 59 7a 66 66 74 4a 72 69 54 49 6c 71 72 78 48 67 71 48 39 59 65 51 76 6a 64 4e 74 63 6e 68 30 34 69 6e 54 46 30 4b 56 67 7a 57 68 76 4f 54 5a 65 6c 42 4b 6d 2f 75 66 4c 47 6e 61 6f 34 47 56 41 39 70 2b 6b 6e 78 42 61 49 4e 33 59 68 46 6a 64 52 51 53 34 76 6b 68 61 70 61 51 56 45 65 36 54 32 4f 62 54 45 68 6d 74 32 53 42 53 53 6d 55 50 58 44 4e 2f 4a 62 36 31 7a 38 44 32 52 55 6f 42 35 2b 4a 53 65 37 70 79 6a 4e 6f 41 4b 43 4a 56 48 4e 51 4a 36 4b 76 44 34 56 4f 74 42 49 63 34 6b 71 4b 45 32 62 76 4d 2f 6d 55 48 37 31 31 35 41 6a 58 72 4e 31 31 48 72 64 53 77 53 4d 55 7a 33 6e 30 4d 64 78 72 7a 2b 6e 5a 77 43 75 6d 78 61 49 50 43 74 79 76 66 31 33 63 39 49 34 57 45 63 59 63 42 5a 4f 6b 67 46 61 5a 79 4e 72 73 6b 63 47 4d 6a 33 38 70 79 49 6f 4f 51 70 34 56 4e 2f 49 70 2f 72 37 73 43 74 6d 74 30 56 37 70 36 35 62 64 2b 4d 74 73 74 43 66 4c 65 42 75 48 6f 59 42 36 47 38 49 31 62
     </pre>
     <pre>
     66 48 4b 41 5a 64 42 7a 51 76 65 73 33 74 38 42 35 76 6d 56 73 6f 4c 4b 7a 66 4c 58 69 54 4d 63 43 2b 2f 75 66 73 4e 59 4a 75 35 62 6b 4f 4a 33 64 51 53 65 2b 35 4f 54 72 6a 31 44 6e 68 2f 4c 35 2f 73 2f 59 58 55 68 76 6d 65 6b 78 6b 79 77 42 69 51 4a 49 4b 4f 44 48 61 43 73 35 31 39 63 57 79 73 7a 6c 6d 50 72 6a 4b 4c 32 4b 42 5a 73 54 41 4e 44 6a 31 56 77 72 35 63 5a 66 76 32 67 7a 4e 73 55 6b 4b 38 4b 30 55 43 38 4c 67 4c 64 50 37 63 4b 47 31 33 39 32 32 71 36 2b 37 6c 4b 77 43 5a 56 6b 36 51 53 6c 30 51 4e 6e 39 6c 31 6e 30 70 36 63 6c 61 73 69 6b 49 69 33 30 36 64 44 66 36 45 33 62 73 67 59 65 65 6a 4e 55 53 2b 6a 6c 6b 58 66 61 34 43 48 58 30 56 66 5a 33 4b 66 4f 62 74 5a 64 6a 39 77 71 6b 35 43 36 45 51 4e 6b 69 33 48 76 57 49 74 38 71 5a 5a 72 70 50 73 39 49 49 42 38 43 73 50 6a 44 4f 38 70 62 57 56 6d 38 42 4b 74 67 32 4a 66 69 45 7a 36 70 58 6b 68 35 32 36 4f 4d 46 6f 4b 36 69 79 77 4f 2f 43 52 37 44 68 71 62 4b 49 39 47 38 31 39 31 78 76 36 6d 30 44 6b 66 71 78 41 71 57 39 5a 6f 65 6b 4c 43 61
     </pre>
     <pre>
     4a 46 43 47 71 48 47 6d 6d 39 63 6f 69 48 79 41 31 54 76 4f 30 6a 43 62 6c 57 6f 6d 45 65 30 53 51 56 67 59 50 64 43 79 34 6a 65 74 76 56 67 6b 65 47 58 46 43 6b 68 6a 65 4e 59 76 52 36 63 7a 74 68 53 58 50 45 39 64 36 74 47 75 6f 45 34 79 44 4a 55 39 4a 65 49 6f 76 76 32 39 48 51 32 50 64 6a 35 37 59 4a 32 78 4c 7a 7a 7a 5a 4c 51 79 50 36 44 6a 51 41 4a 38 33 38 32 6a 7a 4f 7a 56 2b 49 4e 6f 74 5a 36 39 46 43 4d 4b 56 42 39 58 4b 63 49 32 4f 4f 57 6a 6b 30 45 62 64 37 6d 62 33 76 77 42 6e 58 50 73 5a 77 43 78 74 46 6f 46 51 7a 52 50 47 70 59 77 35 36 48 77 66 4f 33 57 63 63 6a 71 79 31 55 56 45 70 64 47 4e 51 75 36 59 79 65 73 71 53 72 66 61 63 4c 76 2f 2b 31 51 72 6b 75 32 42 76 43 7a 73 6c 56 58 73 52 6e 57 65 35 4f 49 48 51 49 63 77 36 4b 69 51 62 35 45 73 52 73 62 37 77 41 78 39 4d 75 68 56 4e 72 42 6b 65 4c 62 4e 39 69 2f 50 6d 4e 78 70 77 75 37 4e 79 52 68 46 51 44 6f 36 70 65 2f 6a 2f 49 33 35 6d 6e 74 30 56 70 30 57 32 55 53 77 2b 48 74 71 62 38 6e 47 6c 59 44 77 30 66 43 47 37 4d 6f 4a 51 6c 2b
     </pre>
     <pre>
     34 68 68 2f 5a 31 67 78 72 2b 30 43 6c 7a 32 66 47 71 35 68 5a 62 4b 37 41 61 4f 2f 78 56 31 63 32 56 74 6c 6b 4e 42 71 79 33 49 69 74 69 6c 50 54 4a 35 51 35 78 36 6f 34 5a 62 4d 52 6a 66 74 2b 76 4c 4a 6d 57 44 59 64 30 61 51 50 2f 75 6c 30 2b 2b 44 67 47 2f 51 76 76 2f 4a 79 42 50 6f 57 4a 70 51 57 79 39 4e 43 6b 48 45 58 30 66 4e 55 39 4f 72 47 54 44 69 6e 59 77 75 7a 42 41 30 62 75 49 30 2f 4c 6d 4f 2b 6a 5a 62 4d 39 64 33 5a 4d 42 78 35 4e 46 79 4a 4f 55 4a 55 6f 47 52 37 6c 2b 36 6f 70 68 37 63 37 2b 4f 58 56 72 4c 6e 35 48 6c 77 69 48 76 30 6b 44 66 43 58 71 37 6f 51 52 30 6c 55 31 2f 44 56 6a 2f 4f 50 6a 6d 78 54 74 6a 42 48 61 63 6d 45 42 70 6f 6b 31 2f 45 6a 67 41 56 6f 4a 6f 4a 30 47 2f 4f 5a 72 5a 72 68 2f 62 31 6f 4b 62 61 4e 6b 6b 78 69 6c 6f 69 6f 63 67 45 6d 67 32 30 53 31 31 33 32 6f 49 55 73 51 6c 51 4f 51 77 35 51 75 59 38 6b 72 5a 51 44 4d 78 61 74 73 7a 32 4b 53 73 79 66 59 4a 32 7a 73 52 64 74 31 38 47 49 66 6d 57 7a 42 65 74 66 5a 72 4e 48 4a 66 50 6c 31 54 43 76 4a 6e 74 31 42 54
     </pre>
     <pre>
     62 4d 65 2f 75 4c 63 55 76 36 32 43 6f 47 74 51 56 4b 50 71 53 36 78 30 59 79 48 43 45 64 4f 70 30 79 48 6c 6c 45 4d 6c 31 61 41 41 62 64 66 4a 70 72 6b 66 77 43 76 44 39 70 6b 55 64 6d 52 49 48 4c 33 43 5a 66 54 67 5a 73 74 33 4d 6b 6c 71 34 33 30 5a 65 4a 39 37 2b 61 76 52 56 5a 75 37 53 30 35 63 54 56 34 44 75 4f 79 4f 62 6d 6b 70 56 70 77 65 61 43 67 4e 49 63 51 76 30 74 41 48 45 54 45 2f 68 4e 73 74 4f 55 77 34 59 58 73 52 63 71 46 79 33 32 37 45 4b 4f 75 51 49 71 4a 38 41 69 56 7a 75 5a 6f 42 2b 6b 4f 73 52 73 33 36 46 46 79 34 44 42 51 6f 73 42 58 71 56 48 48 6c 4b 4f 42 4f 77 43 2b 2f 2f 36 65 58 38 79 47 51 64 48 7a 66 69 47 61 2b 46 34 50 71 48 51 4c 79 6c 42 6b 4b 5a 45 6c 4a 6c 6d 69 4b 45 6d 2b 33 46 41 51 77 70 61 4e 37 53 76 78 49 50 4a 46 55 6f 45 37 53 4b 42 41 65 70 7a 5a 32 45 59 72 57 57 78 62 66 6b 50 61 59 4e 79 5a 77 52 4d 30 54 63 53 42 74 31 31 46 41 58 37 6f 4b 73 4c 6d 67 50 62 41 74 30 46 72 46 77 55 33 4d 36 4b 42 39 79 45 67 55 64 44 4c 58 70 5a 77 43 4a 53 72 50 34 36 54 34
     </pre>
     <pre>
     72 31 41 65 59 59 58 32 42 62 71 43 35 4e 52 33 2f 61 56 6f 7a 31 31 43 34 38 72 59 47 79 41 49 71 35 37 39 7a 78 76 48 4a 53 33 6b 66 48 6c 63 32 68 77 4c 49 59 71 50 76 32 54 54 6e 6f 4c 6b 51 49 64 67 48 79 74 44 72 59 4e 78 30 76 43 43 65 2f 39 78 66 43 66 62 45 34 34 4d 4a 58 5a 72 75 30 32 71 6d 63 43 4b 56 34 6b 5a 58 59 4a 6e 67 49 6d 49 69 50 76 30 42 64 35 57 38 42 44 35 69 64 52 33 6d 50 65 6f 75 77 70 6d 72 2b 2b 64 4b 35 41 59 49 73 6a 36 47 66 63 42 4a 6e 54 6f 57 31 4e 6e 63 6f 31 63 6f 41 37 5a 74 76 6a 42 79 51 3d 3d
     </pre>
     </details>
   
#### 9. Decode each block of ciphertext bytes from base64 using <a href=https://cryptii.com/pipes/hex-to-base64>Cryptii</a>, then combine them into a single string:
   - <details>
     <summary>Decoded ciphertext message</summary>
     <pre>
     57 85 8f b7 ca ff 51 cd 78 1a 99 2c ca bd a2 e2 56 1a b8 1e a4 6b 87 19 de ab a7 b9 82 73 61 f7 4d 63 37 df b4 9a e2 4c 89 6a af 11 e0 a8 7f 58 79 0b e3 74 db 5c 9e 1d 38 8a 74 c5 d0 a5 60 cd 68 6f 39 36 5e 94 12 a6 fe e7 cb 1a 76 a8 e0 65 40 f6 9f a4 9f 10 5a 20 dd d8 84 58 dd 45 04 b8 be 48 5a a5 a4 15 11 ee 93 d8 e6 d3 12 19 ad d9 20 52 4a 65 0f 5c 33 7f 25 be b5 cf c0 f6 45 4a 01 e7 e2 52 7b ba 72 8c da 00 28 22 55 1c d4 09 e8 ab c3 e1 53 ad 04 87 38 92 a2 84 d9 bb cc fe 65 07 ef 5d 79 02 35 eb 37 5d 47 ad d4 b0 48 c5 33 de 7d 0c 77 1a f3 fa 76 70 0a e9 b1 68 83 c2 b7 2b df d7 77 3d 23 85 84 71 87 01 64 e9 20 15 a6 72 36 bb 24 70 63 23 df ca 72 22 83 90 a7 85 4d fc 8a 7f af bb 02 b6 6b 74 57 ba 7a e5 b7 7e 32 db 2d 09 f2 de 06 e1 e8 60 1e 86 f0 8d 5b 7c 72 80 65 d0 73 42 f7 ac de df 01 e6 f9 95 b2 82 ca cd f2 d7 89 33 1c 0b ef ee 7e c3 58 26 ee 5b 90 e2 77 75 04 9e fb 93 93 ae 3d 43 9e 1f cb e7 fb 3f 61 75 21 be 67 a4 c6 4c b0 06 24 09 20 a3 83 1d a0 ac e7 5f 5c 5b 2b 33 96 63 eb 8c a2 f6 28 16 6c 4c 03 43 8f 55 70 af 97 19 7e fd a0 cc db 14 90 af 0a d1 40 bc 2e 02 dd 3f b7 0a 1b 5d fd db 6a ba fb b9 4a c0 26 55 93 a4 12 97 44 0d 9f d9 75 9f 4a 7a 72 56 ac 8a 42 22 df 4e 9d 0d fe 84 dd bb 20 61 e7 a3 35 44 be 8e 59 17 7d ae 02 1d 7d 15 7d 9d ca 7c e6 ed 65 d8 fd c2 a9 39 0b a1 10 36 48 b7 1e f5 88 b7 ca 99 66 ba 4f b3 d2 08 07 c0 ac 3e 30 ce f2 96 d6 56 6f 01 2a d8 36 25 f8 84 cf aa 57 92 1e 76 e8 e3 05 a0 ae a2 cb 03 bf 09 1e c3 86 a6 ca 23 d1 bc d7 dd 71 bf a9 b4 0e 47 ea c4 0a 96 f5 9a 1e 90 b0 9a 24 50 86 a8 71 a6 9b d7 28 88 7c 80 d5 3b ce d2 30 9b 95 6a 26 11 ed 12 41 58 18 3d d0 b2 e2 37 ad bd 58 24 78 65 c5 0a 48 63 78 d6 2f 47 a7 33 b6 14 97 3c 4f 5d ea d1 ae a0 4e 32 0c 95 3d 25 e2 28 be fd bd 1d 0d 8f 76 3e 7b 60 9d b1 2f 3c f3 64 b4 32 3f a0 e3 40 02 7c df cd a3 cc ec d5 f8 83 68 b5 9e bd 14 23 0a 54 1f 57 29 c2 36 38 e5 a3 93 41 1b 77 b9 9b de fc 01 9d 73 ec 67 00 b1 b4 5a 05 43 34 4f 1a 96 30 e7 a1 f0 7c ed d6 71 c8 ea cb 55 15 12 97 46 35 0b ba 63 27 ac a9 2a df 69 c2 ef ff ed 50 ae 4b b6 06 f0 b3 b2 55 57 b1 19 d6 7b 93 88 1d 02 1c c3 a2 a2 41 be 44 b1 1b 1b ef 00 31 f4 cb a1 54 da c1 91 e2 db 37 d8 bf 3e 63 71 a7 0b bb 37 24 61 15 00 e8 ea 97 bf 8f f2 37 e6 69 ed d1 5a 74 5b 65 12 c3 e1 ed a9 bf 27 1a 56 03 c3 47 c2 1b b3 28 25 09 7e e2 18 7f 67 58 31 af ed 02 97 3d 9f 1a ae 61 65 b2 bb 01 a3 bf c5 5d 5c d9 5b 65 90 d0 6a cb 72 22 b6 29 4f 4c 9e 50 e7 1e a8 e1 96 cc 46 37 ed fa f2 c9 99 60 d8 77 46 90 3f fb a5 d3 ef 83 80 6f d0 be ff c9 c8 13 e8 58 9a 50 5b 2f 4d 0a 41 c4 5f 47 cd 53 d3 ab 19 30 e2 9d 8c 2e cc 10 34 6e e2 34 fc b9 8e fa 36 5b 33 d7 77 64 c0 71 e4 d1 72 24 e5 09 52 81 91 ee 5f ba a2 98 7b 73 bf 8e 5d 5a cb 9f 91 e5 c2 21 ef d2 40 df 09 7a bb a1 04 74 95 4d 7f 0d 58 ff 38 f8 e6 c5 3b 63 04 76 9c 98 40 69 a2 4d 7f 12 38 00 56 82 68 27 41 bf 39 9a d9 ae 1f db d6 82 9b 68 d9 24 c6 29 68 8a 87 20 12 68 36 d1 2d 75 df 6a 08 52 c4 25 40 e4 30 e5 0b 98 f2 4a d9 40 33 31 6a db 33 d8 a4 ac c9 f6 09 db 3b 11 76 dd 7c 18 87 e6 5b 30 5e b5 f6 6b 34 72 5f 3e 5d 53 0a f2 67 b7 50 53 6c c7 bf b8 b7 14 bf ad 82 a0 6b 50 54 a3 ea 4b ac 74 63 21 c2 11 d3 a9 d3 21 e5 94 43 25 d5 a0 00 6d d7 c9 a6 b9 1f c0 2b c3 f6 99 14 76 64 48 1c bd c2 65 f4 e0 66 cb 77 32 49 6a e3 7d 19 78 9f 7b f9 ab d1 55 9b bb 4b 4e 5c 4d 5e 03 b8 ec 8e 6e 69 29 56 9c 1e 68 28 0d 21 c4 2f d2 d0 07 11 31 3f 84 db 2d 39 4c 38 61 7b 11 72 a1 72 df 6e c4 28 eb 90 22 a2 7c 02 25 73 b9 9a 01 fa 43 ac 46 cd fa 14 5c b8 0c 14 28 b0 15 ea 54 71 e5 28 e0 4e c0 2f bf ff a7 97 f3 21 90 74 7c df 88 66 be 17 83 ea 1d 02 f2 94 19 0a 64 49 49 96 68 8a 12 6f b7 14 04 30 a5 a3 7b 4a fc 48 3c 91 54 a0 4e d2 28 10 1e a7 36 76 11 8a d6 5b 16 df 90 f6 98 37 26 70 44 cd 13 71 20 6d d7 51 40 5f ba 0a b0 b9 a0 3d b0 2d d0 5a c5 c1 4d cc e8 a0 7d c8 48 14 74 32 d7 a5 9c 02 25 2a cf e3 a4 f8 af 50 1e 61 85 f6 05 ba 82 e4 d4 77 fd a5 68 cf 5d 42 e3 ca d8 1b 20 08 ab 9e fd cf 1b c7 25 2d e4 7c 79 5c da 1c 0b 21 8a 8f bf 64 d3 9e 82 e4 40 87 60 1f 2b 43 ad 83 71 d2 f0 82 7b ff 71 7c 27 db 13 8e 0c 25 76 6b bb 4d aa 99 c0 8a 57 89 19 5d 82 67 80 89 88 88 fb f4 05 de 56 f0 10 f9 89 d4 77 98 f7 a8 bb 0a 66 af ef 9d 2b 90 18 22 c8 fa 19 f7 01 26 74 e8 5b 53 67 72 8d 5c a0 0e d9 b6 f8 c1 c9
     </pre>
     </details>
     
#### 10. Use a hex editor to place the ciphertext message bytes into a file:
   - <details>
     <summary>Ciphertext file</summary>
     <a href=https://github.com/aayushdhiman/techman/blob/main/WireShark_CTF/encrypted_message.txt><code>encrypted_message.txt</code></a>
     </details>
   
#### 10. Decrypt the ciphertext message file with AES using <a href=http://aes.online-domain-tools.com/>OnlineDomainTools</a> and the encryption key:
   - Change the input type to `file` and upload the ciphertext message file.
   - Change the mode to `CBC (cipher block chaining)`.
   - Change the key type to `Hex` and enter the encryption key.
   - Set the initialization vector to `0`.
   - Decrypt the message.
   - <details>
     <summary>Plaintext Message:</summary>
     <pre>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultrices elit non enim faucibus, quis molestie dolor molestie. Pellentesque congue mollis pharetra. Ut ultrices purus est, sed vulputate purus euismod vitae. Curabitur nec ipsum sed neque maximus euismod in eget ex. Fusce arcu libero, vestibulum sit amet metus laoreet, dictum tempus velit. Integer tempor dolor sodales sapien vulputate, vel placerat massa laoreet. Quisque imperdiet consequat quam, in luctus justo efficitur ac. Phasellus maximus venenatis massa sit amet efficitur. Mauris congue, dui vel gravida venenatis, dui libero luctus erat, quis semper erat est non nunc.[Nothing to see here]Sed accumsan mi sed erat convallis volutpat nec ut orci. Duis blandit maximus dolor id vestibulum. Sed vel sapien ut odio volutpat venenatis. Aliquam dolor eros, maximus sit amet tellus viverra, pharetra laoreet lacus. Morbi pulvinar est lectus, vitae fermentum dui maximus id. Quisque orci nisi, viverra faucibus ultricies id, tristique in arcu. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi ut aliquet neque, ac porttitor lorem.[KEY: 7 5 4 7 7 0 3 0]Maecenas vehicula luctus libero quis venenatis. Nullam vestibulum ex a neque dignissim facilisis. Aenean feugiat velit quis facilisis tristique. Sed id convallis odio. Nulla a mi tempus arcu pharetra pellentesque. Fusce tellus orci, consectetur quis enim sed, laoreet.</pre>
   </details>

---

Once decrypted, the plaintext message contains the key: [KEY: 7 5 4 7 7 0 3 0]

<details>
  <summary>Plaintext Message:</summary>
  <pre>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultrices elit non enim faucibus, quis molestie dolor molestie. Pellentesque congue mollis pharetra. Ut ultrices purus est, sed vulputate purus euismod vitae. Curabitur nec ipsum sed neque maximus euismod in eget ex. Fusce arcu libero, vestibulum sit amet metus laoreet, dictum tempus velit. Integer tempor dolor sodales sapien vulputate, vel placerat massa laoreet. Quisque imperdiet consequat quam, in luctus justo efficitur ac. Phasellus maximus venenatis massa sit amet efficitur. Mauris congue, dui vel gravida venenatis, dui libero luctus erat, quis semper erat est non nunc.
[Nothing to see here]
Sed accumsan mi sed erat convallis volutpat nec ut orci. Duis blandit maximus dolor id vestibulum. Sed vel sapien ut odio volutpat venenatis. Aliquam dolor eros, maximus sit amet tellus viverra, pharetra laoreet lacus. Morbi pulvinar est lectus, vitae fermentum dui maximus id. Quisque orci nisi, viverra faucibus ultricies id, tristique in arcu. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi ut aliquet neque, ac porttitor lorem.
[KEY: 7 5 4 7 7 0 3 0]
Maecenas vehicula luctus libero quis venenatis. Nullam vestibulum ex a neque dignissim facilisis. Aenean feugiat velit quis facilisis tristique. Sed id convallis odio. Nulla a mi tempus arcu pharetra pellentesque. Fusce tellus orci, consectetur quis enim sed, laoreet.</pre>
</details>

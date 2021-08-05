Provided was a readme file, a pdf file documenting the communication and encryption process, and a pcap file containing the encrypted packets.

The first step was to examine the documentation and determine how the client and the AP communicate and authenticate.

---

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

### Reversing the encryption:
  1. Determine the authentication magic from the probe response.
  2. Decrypt the `AP_HMAC` and the router password using the authorization magic.
  3. Decrypt the `Client_HMAP` using the `AP_HMAC`.
  4. Find the MD5 hash value of `Client_HMAC + AP_HMAC` to determine the encryption key.
  5. Collect and decode each block of ciphertext.
  6. Decrypt the ciphertext message using the encryption key.

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

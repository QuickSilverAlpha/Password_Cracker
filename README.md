# Password_Cracker
The cracker tries to extract passwords from three different password public dumps (plaintext and hashed).

## Dump 1: Yahoo

The first file is from the Yahoo leak. The name of the file is 'password.file'. On examination, I can see that the file is a MySQL database dump, and the passwords are in plaintext, with no encryption or hashing.
I need to parse this file to get the passwords. Following are the steps that I took to parse the file:
  1. Divide the files into chunks to get the relevant part that has the email and the password dump.
  2. Iterate over that chunk line by line, starting from index six as the first password appears on that line.
  3. Split the characters at ':' to get the password at the second index.
Since this dump has the password stored in plaintext, it is easiest to retrieve. I had to parse the dump. The result is in **dump_yahoo.txt**.

## Dump 2: LinikedIn

The second file is from the LinkedIn leak. The name of the file is 'SHA1.txt'. On examination, I can see that the file has 40 hexadecimal digits and 160bits SHA1 hashes. Though the SHA1 is a cryptographically broken algorithm, it will take me months to crack it. Hence, I used a dictionary of the most common passwords to match the list's passwords.
I used two different dictionaries - the one obtained from the above yahoo plaintext word list and the second, rockyou.txt word list, which is the most common word list comprising a massive collection of leaked passwords.
  - **Yahoo word list:**
  The method is to run through the list of the plaintext word list, hash it using SHA1 and compare the hashes. The corresponding plaintext word is the password if there is a match.
      1. I created a python dictionary of all the passwords in the SHA1.txt and stored it in the memory.
      2. Then I read the file containing yahoo wordlist (yahoo_word_list.txt, refer source_linkedin folder) line by line, hashed each password with SHA1 using hashlib      python library and looked it up in the python dictionary.
      3. In case of a key match, the corresponding word is the password.

  - **Rockyou word list:**
  Surprisingly, I did not find many matches from this list using the above methodology. Upon careful inspection, I saw that the 0s substituted the first five most significant digits. For instance, 12345, when hashed with SHA1, gives 7c4a8d09ca3762af61e59520943dc26494f8941b but in the SHA1.txt it is stored as 00000d09ca3762af61e59520943dc26494f8941b. So, for this, I started comparing the last 35 digits and found numerous matches. (Refer cracked_dump_rockyou_SHA1.txt in source_linkedin)
  This stood comparatively more complex than retrieving the yahoo dump from plain text. The result is in **cracked_dump_SHA1.txt**.


## Dump 3: Formspring
The third file is from the Formspring leak. The name of the file is 'formspring.txt'. On examination, I can see that the file has 64 hexadecimal digits and 256bits SHA256 hashes. The SHA-256 hashing algorithm is irreversible. Hence, I used a dictionary of the most common passwords to match the list's passwords. Surprisingly, there was no match in comparing the SHA-256 hashed passwords from the wordlist with the list of hashes in formspring.txt. On further investigation online, I saw that these hashes are using salt, a random number between 00-99 prepended to the password before hashing. Therefore, the task became challenging as each word in the word list must be prepended with salt and compared, making the possible combination increase 100x.
Here I used the dictionary obtained from the above yahoo plaintext word list. The method is to run through the list of the plaintext word list, prepend the salt from 00-99 to the word, hash it using SHA256 and compare the hashes. To elaborate, the word 123456 became 00123456, 01123456, 02123456 and so on. The corresponding plaintext word is the password if there is a match.
  1. I created a python dictionary of all possible hashes obtained after adding the salt.
  2. Then I read the file (formspring.txt) containing hashes line by line and looked it up in the python dictionary.
  3. In case of a key match, the corresponding word is the password.

The SHA-256 encryption using a salt made it the most complex problem to solve out of all the three. Even simple passwords like 123456 became 100x challenging to crack. The result is in **cracked_dump_SHA256.txt**.

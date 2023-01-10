import os
import hashlib
import traceback

PASSWD_FILE_NAME = 'yahoo_word_list.txt'
HASHED_PWD_FILE = 'formspring.txt'
CRACKED_DUMP = 'cracked_dump_SHA256.txt'


def create_pass_dict_with_salt():

    # absolute path of the passwd file
    pwd_file_abs_path = os.path.join(os.getcwd(), PASSWD_FILE_NAME)
    hashed_pwd_dict = {}    # Contains the hash of salted password ("<salt rand(00-99)><pwd>": pwd) from the word list
    salt_list = [str(salt).zfill(2) for salt in range(100)]  # Create a list of 00-99 to prepend on the password

    try:
        # read word list
        with open(pwd_file_abs_path, 'r', errors='ignore') as pwd_fhandle:
            try:
                for line in pwd_fhandle:
                    try:

                    # Check if line is not empty:
                        if line:
                            if line[-1] == '\n':
                                pwd = line[:-1]
                            else:
                                pwd = line

                            # Adding salt to password and adding it to the dict
                            for salt in salt_list:
                                try:
                                    salted_pwd = salt + pwd
                                    # print(salted_pwd)
                                    hash_obj = hashlib.sha256()
                                    hash_obj.update(salted_pwd.encode('utf-8'))
                                    sha256_str = hash_obj.hexdigest()
                                    print(sha256_str)
                                    hashed_pwd_dict[sha256_str] = pwd

                                except:
                                    traceback.print_exc()

                    except:
                        traceback.print_exc()

            except:
                traceback.print_exc()

    except FileNotFoundError:
        print("{} doesnt exist!".format(PASSWD_FILE_NAME))
        traceback.print_exc()

    except:
        traceback.print_exc()
    finally:
        print("Returning dict")
        return hashed_pwd_dict


def read_formspring_hashes():

    formspring_file_path = os.path.join(os.getcwd(), HASHED_PWD_FILE)
    formspring_hash_list = []       # Will store the hashes in list

    try:
        with open(formspring_file_path, 'r') as hashed_pwd_fhandle:
            try:

                for line in hashed_pwd_fhandle:

                    # Check if line is not empty:
                    if line:
                        if line[-1] == '\n':
                            formspring_hash = line[:-1]
                        else:
                            formspring_hash = line

                        print(formspring_hash)
                        formspring_hash_list.append(formspring_hash)

            except:
                traceback.print_exc()

    except FileNotFoundError:
        print("{} doesnt exist!".format(PASSWD_FILE_NAME))
        traceback.print_exc()

    except:
        traceback.print_exc()
    finally:
        return formspring_hash_list


def dump_cracked_pwd(cracked_pwd_list):

    cracked_dump_abs_path = os.path.join(os.getcwd(), CRACKED_DUMP)

    try:
        with open(cracked_dump_abs_path, 'w') as dump_fhandle:
            if cracked_pwd_list:    # check if the list is not empty

                for pwd_tuple in cracked_pwd_list:
                    try:
                        pwd_str = '{} {}\n'.format(pwd_tuple[0], pwd_tuple[1])
                        dump_fhandle.write(pwd_str)

                    except:
                        traceback.print_exc()
            else:
                print('Nothing to write to {}'.format(cracked_dump_abs_path))

    except PermissionError:
        print("No permission to write file {}!".format(CRACKED_DUMP))
        traceback.print_exc()

    except:
        traceback.print_exc()


if __name__ == '__main__':

    cracked_pass_list = []  # This will store the cracked password tuples (hash, matched password)
    try:
        hashed_pwd_dict = create_pass_dict_with_salt()
        formspring_hash_list = read_formspring_hashes()

        if hashed_pwd_dict and formspring_hash_list:        # Check if not empty

            pwd_counter = 0     # Count the passwords found
            for formspring_hash in formspring_hash_list:
                try:
                    # check if hash exists in the dict
                    if hashed_pwd_dict.get(formspring_hash, None):
                        print("Found Match!")
                        cracked_tuple = (formspring_hash, hashed_pwd_dict[formspring_hash])
                        print(cracked_tuple)
                        cracked_pass_list.append(cracked_tuple)
                        pwd_counter += 1

                    if pwd_counter == 100:      # Just looking for 100 matches
                        break

                except:
                    traceback.print_exc()

            if cracked_pass_list:           # Checking if it's not empty
                dump_cracked_pwd(cracked_pass_list)

    except:
        traceback.print_exc()

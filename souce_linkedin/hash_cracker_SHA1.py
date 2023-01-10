import os
import hashlib
import traceback

PASSWD_FILE_NAME = 'yahoo_word_list.txt'
HASHED_PWD_FILE = 'SHA1.txt'
CRACKED_DUMP = 'cracked_dump_SHA1.txt'


def create_pass_list():

    pass_abs_name = os.path.join(os.getcwd(), PASSWD_FILE_NAME)
    pass_list = []  # Will contain the list of passwords after reading from word list

    try:
        # read word list
        with open(pass_abs_name, 'r', errors='ignore') as pwd_handle:

            try:
                for line in pwd_handle:
                    try:
                        pass_list.append(line)
                        print(line)
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
        return pass_list


def read_hashes():
    hash_abs_name = os.path.join(os.getcwd(), HASHED_PWD_FILE)
    hash_dict = {}  # Will contain the hashes ({'hash: hash'}) after reading from SHA1.txt

    try:
        # read hashes from SHA1.txt
        with open(hash_abs_name, 'r', errors='ignore') as hash_handle:

            try:
                for line in hash_handle:
                    if '\n' == line[-1]:
                        line = line[:-1]
                    try:
                        hash_dict[line] = line
                        print(line)
                    except:
                        traceback.print_exc()
            except:
                traceback.print_exc()
            pass
    except FileNotFoundError:
        print("{} doesnt exist!".format(HASHED_PWD_FILE))
        traceback.print_exc()

    except:
        traceback.print_exc()
    finally:
        return hash_dict


def dump_cracked_pwd(pwd_list):

    cracked_dump_abs_path = os.path.join(os.getcwd(), CRACKED_DUMP)

    try:
        with open(cracked_dump_abs_path, 'w') as dump_fhandle:
            if pwd_list:
                for pwd_tuple in pwd_list:
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

    try:
        password_list = []
        pass_list = create_pass_list()
        hash_dict = read_hashes()

        if pass_list and hash_dict:     # Checking if it returns empty
            pwd_counter = 0     # Count the passwords found
            for pwd in pass_list:
                try:
                    if '\n' == pwd[-1]:
                        pwd = pwd[:-1]
                    hash_obj = hashlib.sha1()
                    hash_obj.update(pwd.encode('utf-8'))
                    sha1_str = hash_obj.hexdigest()

                    if hash_dict.get(sha1_str, None):
                        print('Match Found!')
                        password_tuple = (hash_dict[sha1_str], pwd)
                        password_list.append(password_tuple)
                        print(password_tuple)
                        pwd_counter += 1

                    if pwd_counter == 100:          # Just looking for 100 matches
                        break

                except:
                    traceback.print_exc()

            if password_list:           # Checking if its empty
                dump_cracked_pwd(password_list)
        else:
            print('Nothing to compare')

    except:
        traceback.print_exc()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

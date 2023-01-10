import os
import re
import traceback

PASSWD_FILE_NAME = 'password.file'
DUMP_FILE = 'dump_yahoo.txt'


def read_and_parse():

    # The function will read and parse the password.file
    pwd_file_name = os.path.join(os.getcwd(), PASSWD_FILE_NAME)
    file_content = None
    relevant_chunk = None

    try:
        with open(pwd_file_name, 'r', encoding='cp1252') as pwd_fhandle:

            # read the file as a whole
            file_content = pwd_fhandle.read()

        if file_content:

            # splitting the file using two patterns to get the relevant chunk
            file_chunks = re.split(r"--------------------------------\n|---------------\n", file_content)

            # checking if the split happened correctly for the password.file. Will need to modify for other files
            if len(file_chunks) == 5:
                relevant_chunk = file_chunks[3]

        else:
            print("Nothing to process! File read failure for file {}".format(PASSWD_FILE_NAME))

    except FileNotFoundError:
        print("{} doesnt exist!".format(PASSWD_FILE_NAME))
        traceback.print_exc()

    except:
        traceback.print_exc()

    finally:
        return relevant_chunk


def process_and_dump_pwds(relevant_chunk):
    try:
        # Open file handle
        with open(DUMP_FILE, 'w') as dump_fhandle:
            # Process the relevant chunk
            # Split the relevant chunk with \n to get the lines for processing
            relevant_chunk_lines = relevant_chunk.split("\n")

            # Iterate through relevant lines starting at 6th element
            pwd_counter = 0
            for index in range(6, len(relevant_chunk_lines)-1):
                # check of chunk isn't empty
                if relevant_chunk_lines[index]:
                    creds_list = relevant_chunk_lines[index].split(':')

                    # check if it is not \t or \n or without password
                    if len(creds_list) > 1:
                        final_pwd_str = "{} {}\n".format(creds_list[2].strip(), creds_list[2].strip())

                        # dump pwd into dump file
                        dump_fhandle.write(final_pwd_str)
                        pwd_counter += 1

                    if pwd_counter == 100:
                        break

    except PermissionError:
        print("No permission to write file {}!".format(PASSWD_FILE_NAME))
        traceback.print_exc()

    except:
        traceback.print_exc()


if __name__ == '__main__':
    try:
        # parse the file and retrieve the portion of file that has the creds for further processing
        relevant_chunk = read_and_parse()

        # check if relevant chunk where unames and pwds are present are there
        if relevant_chunk:
            process_and_dump_pwds(relevant_chunk)
        else:
            print("Failure! Nothing to process!")

    except:
        traceback.print_exc()

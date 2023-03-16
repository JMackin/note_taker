import gnupg
import os


def start_gpg():


    gpg = gnupg.GPG(gnupghome="~/.gnupg")

    if not os.path.exists('./encrypted_out/'):
        os.mkdir('./encrypted_out')
    if not os.path.exists('./decrypted_out/'):
        os.mkdir('./decrypted_out')

    return gpg


# TAKES A FILEPATH TO GPG KEY FILE
def import_keys(key: str):

    gpg = start_gpg()

    import_res = gpg.import_keys_file(key)

    print(import_res)


# PATH TO FILE TO BE ENCRYPTED AND RECEIVER
def encrypt_it_file(file: str, usr: str):

    gpg = start_gpg()

    outfile_name = f'{file.split("/")[-1]}.gpg'

    with open(file, 'rb') as infile:
        out_stream = gpg.encrypt_file(infile, usr, output=f'./encrypted_out/{outfile_name}')
        print(f"Gpg success?:{out_stream.ok}\nstatus:{out_stream.status}")



# TEXT STRING TO BE ENCRYPTED AND RECEIVER
# OPTIONAL PARAMS
#   - outfile_name: IF PROVIDED STREAM IS WRITTEN TO A FILE WITH GIVEN NAME AS ./encrypted_out/outfile_name.asc
#   - as_armor: RETURNS STREAM AS ASCII, EITHER OUTPUTTING TO FILE OR TO A STRING OBJECT
def encrypt_it_textstream(intext: str, usr: str, outfile_name=None):

    gpg = start_gpg()

    if outfile_name is not None:
        with open(f'./encrypted_out/{outfile_name}.asc', 'wb') as outf:
            out_stream = gpg.encrypt(intext, usr)
            print(f"Gpg success?:{out_stream.ok}\nstatus:{out_stream.status}")
            if out_stream.ok:
                outf.write(out_stream.data)
        return None
    else:
        out_stream = gpg.encrypt(intext, usr)
        print(f"Gpg success?:{out_stream.ok}")
        if out_stream.ok:
            return out_stream.data


def decrypt_it(input_str: str, passwd_file=None, outfile_name=None):

    gpg = start_gpg()

    # IF INPUT IS A FILE PATH
    if len(input_str) < 40 and os.path.exists(input_str):
        # IF PATH TO A FILE CONTAINING PASSWORD IS GIVEN
        if passwd_file is not None:
            with open(passwd_file, 'r') as passwd:
                # IF OUTPUT FILENAME IS GIVEN
                if outfile_name is not None:
                    decrypt_out = gpg.decrypt_file(input_str, passphrase=passwd.read(), output=f'decrypted_out/{outfile_name}.txt')
                    print(f'Gpg Success?:{decrypt_out.ok}')

                    print(decrypt_out.status)
                # IF NO OUTPUT FILENAME
                else:
                    decrypt_out = gpg.decrypt_file(input_str, passphrase=passwd.read())
                    print(f'Gpg Success?:{decrypt_out.ok}')
                    return decrypt_out
        # IF NO PASSWORD SUPPLIED
        else:
            # IF OUTPUT FILENAME IS GIVEN
            if outfile_name is not None:
                decrypt_out = gpg.decrypt_file(input_str, output=f'decrypted_out/{outfile_name}.txt')
                print(f'Gpg Success?:{decrypt_out.ok}')
                print({decrypt_out.status})
            # IF NO OUTPUT FILENAME
            else:
                decrypt_out = gpg.decrypt_file(input_str)
                print(f'Gpg Success?:{decrypt_out.ok}')
                return decrypt_out
    # IF INPUT IS A TEXT STRING
    else:
        # IF PATH TO A FILE CONTAINING PASSWORD IS GIVEN
        if passwd_file is not None:
            with open(passwd_file, 'r') as passwd:
                # IF OUTPUT FILENAME IS GIVEN
                if outfile_name is not None:
                    decrypt_out = gpg.decrypt(input_str, passphrase=passwd.read(), output=f'decrypted_out/{outfile_name}.txt')
                    print(f'Gpg Success?:{decrypt_out.ok}')
                # IF NO OUTPUT FILENAME
                else:
                    decrypt_out = gpg.decrypt(input_str, passphrase=passwd.read())
                    print(f'Gpg Success?:{decrypt_out.ok}')
                    return decrypt_out
        # IF NO PASSWORD SUPPLIED
        else:
            # IF OUTPUT FILENAME IS GIVEN
            if outfile_name is not None:
                decrypt_out = gpg.decrypt(input_str, output=f'decrypted_out/{outfile_name}.txt')
                print(f'Gpg Success?:{decrypt_out.ok}')
            # IF NO OUTPUT FILENAME
            else:
                decrypt_out = gpg.decrypt(input_str)
                print(f'Gpg Success?:{decrypt_out.ok}')
                return decrypt_out


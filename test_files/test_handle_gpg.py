import os

import handle_gpg as hgpg
import os

print(os.getcwd())
hgpg.import_keys('keys/dbajlm_pub.asc')
#
# f = open('test_gpg_file.txt', 'w')
# f.write('Some Text')
# f.close()

# hgpg.encrypt_it_file('test_gpg_file.txt', 'test-gpg-user')

# with open('test2.gpg', 'wb') as outf:
#     outfs = hgpg.encrypt_it_textstream("Sometext", 'dbajlm', as_armor=False)
#     outf.write(outfs)

outstream = hgpg.encrypt_it_file("testlast2.txt", 'test-gpg-user-2')

print(hgpg.decrypt_it('encrypted_out/testlast2.txt.gpg', outfile_name='ass'))

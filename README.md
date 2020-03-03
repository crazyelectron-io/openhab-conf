# openhab-conf: Production configuration, including git-crypt

## Using git-crypt

### Prerequisites

Install GPG (on Linux, this is probably already installed)
Install git-crypt
Clone the repo git

```bash
git clone https://github.com/AGWA/git-crypt.git
cd /path/to/git-crypt
make
git-crypt --version
```

### Encrypt files

```bash
cd openhab2/conf
git-crypt init
touch .gitattributes
```

Specify _future_ files to encrypt in `.gitattributes`

```ini
files-to-encrypt filter=git-crypt diff=git-crypt
```

where _files-to-encrypt_ follows the same syntax as files specified in `.gitignore`

Add files specified in .gitattributes to `openhab-conf` and push up to Git host.
Verify in Git host files are encrypted.

**Attention!**
The local files are still decrypted. But, there is initially no key to unlock the crypt.
This means if the local files are deleted, you will not be able replace them (any replacements will be encrypted).
Also, without a key, no one else can decrypt the files, e.g if on another computer you do git clone `openhab-conf`, the files cannot be decrypted.
As such, it is highly recommended the person who originally encrypted the files creates the first key for the crypt and unlocks it.
From now on, we will refer to this person as `crypt-admin`.
Once `crypt-admin` has created the first key and unlocked the crypt, other authorised users can clone the repository and also decrypt files.
The steps for `crypt-admin` to create the first key and unlock the crypt are below.

### Create a GPG user

`crypt-admin` has to create a GPG user for themselves.

As part of the user creation process, the user will be assigned a public and private GPG key.

```bash
gpg --gen-key
```

Enter _key-type_, _key-size_ in bits, _key-expiration_
Enter _justClouds_, _ron@moerman.online_ - known to Git - GPG automatically creates your USER-ID from these values
Check keys and user have been created

```bash
gpg --list-keys
```

#### Unlock the crypt

Add `crypt-admin`’s GPG user to the crypt git-crypt add-gpg-user "USER-ID"
Verify creation of auto-generated commit Add 1 git-crypt collaborator with git log
Push auto-generated commit up to Git host

```bash
rm -rf /path/to/`openhab-conf`
git clone `openhab-conf`
```

Verify files are encrypted

```bash
git-crypt unlock
```

Verify files are decrypted

### Adding collaborators

`crypt-admin` can now unlock the crypt and decrypt files.
Adding a collaborator.
(Especially as _USER-ID_ contains _key-description_, meaning `crypt-admin` can have, for example, USER-ID equal to James Smith (mac) jsmith@email.com on one machine and James Smith (PC) jsmith@email.com on another.)

To be added, a collaborator should satisfy prerequisites.
Create a GPG user for themselves. Export public key to a file (optionally import on another device and make it trusted).

```bash
$ gpg --list-keys
$ gpg --output _public-key-filename_.gpg --armor --export _public-key-id_
$ gpg --import /path/to/public-key-filename.gpg
$ gpg --list-keys
$ gpg --edit-key <public-key-id>
gpg> sign
gpg> save
```

Unlock the crypt:

```bash
git-crypt unlock
```

Add the key to the crypt:

```bash
git-crypt add-gpg-user _public-key-id_
```

Push auto-generated commit up to Git host.
Pull down `openhab-conf` from Git host

```bash
git-crypt unlock
```

Confirm that the files are decrypted.
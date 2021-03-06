# When updating snapshots, run this file and pipe it into `src/snapshots.txt`
import os
import subprocess
import sys
import hashlib

date = sys.argv[1]

print(date)

if not os.path.isdir('target/dl'):
    os.makedirs('target/dl')

snaps = {
    'macos-i386': 'i686-apple-darwin',
    'macos-x86_64': 'x86_64-apple-darwin',
    'linux-i386': 'i686-unknown-linux-gnu',
    'linux-x86_64': 'x86_64-unknown-linux-gnu',
    'winnt-i386': 'i686-pc-windows-gnu',
    'winnt-x86_64': 'x86_64-pc-windows-gnu',
    'bitrig-x86_64': 'x86_64-unknown-bitrig',
}

for platform in sorted(snaps):
    triple = snaps[platform]
    tarball = 'cargo-nightly-' + triple + '.tar.gz'
    url = 'https://static-rust-lang-org.s3.amazonaws.com/cargo-dist/' + date + '/' + tarball
    dl_path = "target/dl/" + tarball
    ret = subprocess.call(["curl", "-f", "-s", "-o", dl_path, url])
    if ret != 0:
        raise Exception("failed to fetch url")
    h = hashlib.sha1(open(dl_path, 'rb').read()).hexdigest()
    print('  ' + platform + ' ' + h)

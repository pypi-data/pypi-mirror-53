-------------
trydiffoscope
-------------

Uploading
==========

Please also release a signed tarball:

::

    $ VERSION="$(dpkg-parsechangelog -SVersion)"
    $ git archive --format=tar --prefix=trydiffoscope-${VERSION}/ ${VERSION} | bzip2 -9 > trydiffoscope-${VERSION}.tar.bz2
    $ gpg --detach-sig --armor --output=trydiffoscope-${VERSION}.tar.bz2.asc < trydiffoscope-${VERSION}.tar.bz2

And commit them to our LFS repository at https://salsa.debian.org/reproducible-builds/reproducible-lfs

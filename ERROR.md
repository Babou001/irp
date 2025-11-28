C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>docker build -f Dockerfile.prod -t rag-system:prod .
[+] Building 127.3s (8/21)                                                                                                                                                                                               docker:desktop-linux
 => [internal] load build definition from Dockerfile.prod                                                                                                                                                                                0.1s
 => => transferring dockerfile: 3.50kB                                                                                                                                                                                                   0.1s
 => WARN: FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 14)                                                                                                                                                          0.1s
 => [internal] load metadata for docker.io/library/python:3.11-slim                                                                                                                                                                      1.7s
 => [internal] load .dockerignore                                                                                                                                                                                                        0.1s
 => => transferring context: 1.44kB                                                                                                                                                                                                      0.0s
 => CANCELED [internal] load build context                                                                                                                                                                                             124.8s
 => => transferring context: 1.80GB                                                                                                                                                                                                    124.7s
 => [builder 1/6] FROM docker.io/library/python:3.11-slim@sha256:193fdd0bbcb3d2ae612bd6cc3548d2f7c78d65b549fcaa8af75624c47474444d                                                                                                        0.0s
 => CACHED [stage-1  2/12] RUN apt-get update && apt-get install -y     libgomp1     curl     && rm -rf /var/lib/apt/lists/*                                                                                                             0.0s 
 => CACHED [builder 2/6] WORKDIR /app                                                                                                                                                                                                    0.0s 
 => ERROR [builder 3/6] RUN apt-get update && apt-get install -y     build-essential     wget     git     && rm -rf /var/lib/apt/lists/*                                                                                               124.8s 
------
 > [builder 3/6] RUN apt-get update && apt-get install -y     build-essential     wget     git     && rm -rf /var/lib/apt/lists/*:
1.816 Hit:1 http://deb.debian.org/debian trixie InRelease
1.842 Get:2 http://deb.debian.org/debian trixie-updates InRelease [47.3 kB]
2.081 Get:3 http://deb.debian.org/debian-security trixie-security InRelease [43.4 kB]
2.224 Get:4 http://deb.debian.org/debian trixie/main amd64 Packages [9670 kB]
4.303 Get:5 http://deb.debian.org/debian trixie-updates/main amd64 Packages [5412 B]
4.611 Get:6 http://deb.debian.org/debian-security trixie-security/main amd64 Packages [75.6 kB]
7.969 Fetched 9842 kB in 6s (1541 kB/s)
7.969 Reading package lists...
11.96 Reading package lists...
15.09 Building dependency tree...
15.89 Reading state information...
17.08 The following additional packages will be installed:
17.08   binutils binutils-common binutils-x86-64-linux-gnu bzip2 cpp cpp-14
17.08   cpp-14-x86-64-linux-gnu cpp-x86-64-linux-gnu dpkg-dev fakeroot g++ g++-14
17.08   g++-14-x86-64-linux-gnu g++-x86-64-linux-gnu gcc gcc-14
17.08   gcc-14-x86-64-linux-gnu gcc-x86-64-linux-gnu git-man krb5-locales less
17.08   libalgorithm-diff-perl libalgorithm-diff-xs-perl libalgorithm-merge-perl
17.08   libasan8 libatomic1 libbinutils libbrotli1 libc-dev-bin libc6-dev
17.08   libcbor0.10 libcc1-0 libcom-err2 libcrypt-dev libctf-nobfd0 libctf0
17.08   libcurl3t64-gnutls libdpkg-perl libedit2 liberror-perl libexpat1 libfakeroot
17.08   libfido2-1 libfile-fcntllock-perl libgcc-14-dev libgdbm-compat4t64
17.08   libgnutls30t64 libgomp1 libgprofng0 libgssapi-krb5-2 libhwasan0 libidn2-0
17.08   libisl23 libitm1 libjansson4 libk5crypto3 libkeyutils1 libkrb5-3
17.08   libkrb5support0 libldap-common libldap2 liblocale-gettext-perl liblsan0
17.08   libmpc3 libmpfr6 libnghttp2-14 libnghttp3-9 libngtcp2-16
17.08   libngtcp2-crypto-gnutls8 libp11-kit0 libperl5.40 libpsl5t64 libquadmath0
17.09   librtmp1 libsasl2-2 libsasl2-modules libsasl2-modules-db libsframe1
17.09   libssh2-1t64 libstdc++-14-dev libtasn1-6 libtsan2 libubsan1 libunistring5
17.09   libx11-6 libx11-data libxau6 libxcb1 libxdmcp6 libxext6 libxmuu1
17.09   linux-libc-dev make manpages manpages-dev openssh-client patch perl
17.09   perl-modules-5.40 publicsuffix rpcsvc-proto sq xauth xz-utils
17.10 Suggested packages:
17.10   binutils-doc gprofng-gui binutils-gold bzip2-doc cpp-doc gcc-14-locales
17.10   cpp-14-doc debian-keyring debian-tag2upload-keyring g++-multilib
17.10   g++-14-multilib gcc-14-doc gcc-multilib autoconf automake libtool flex bison
17.10   gdb gcc-doc gcc-14-multilib gdb-x86-64-linux-gnu gettext-base git-doc
17.10   git-email git-gui gitk gitweb git-cvs git-mediawiki git-svn libc-devtools
17.10   glibc-doc sensible-utils bzr gnutls-bin krb5-doc krb5-user
17.10   libsasl2-modules-gssapi-mit | libsasl2-modules-gssapi-heimdal
17.10   libsasl2-modules-ldap libsasl2-modules-otp libsasl2-modules-sql
17.10   libstdc++-14-doc make-doc man-browser keychain libpam-ssh monkeysphere
17.10   ssh-askpass ed diffutils-doc perl-doc libterm-readline-gnu-perl
17.10   | libterm-readline-perl-perl libtap-harness-archive-perl
18.82 The following NEW packages will be installed:
18.82   binutils binutils-common binutils-x86-64-linux-gnu build-essential bzip2 cpp
18.82   cpp-14 cpp-14-x86-64-linux-gnu cpp-x86-64-linux-gnu dpkg-dev fakeroot g++
18.82   g++-14 g++-14-x86-64-linux-gnu g++-x86-64-linux-gnu gcc gcc-14
18.82   gcc-14-x86-64-linux-gnu gcc-x86-64-linux-gnu git git-man krb5-locales less
18.82   libalgorithm-diff-perl libalgorithm-diff-xs-perl libalgorithm-merge-perl
18.82   libasan8 libatomic1 libbinutils libbrotli1 libc-dev-bin libc6-dev
18.82   libcbor0.10 libcc1-0 libcom-err2 libcrypt-dev libctf-nobfd0 libctf0
18.82   libcurl3t64-gnutls libdpkg-perl libedit2 liberror-perl libexpat1 libfakeroot
18.82   libfido2-1 libfile-fcntllock-perl libgcc-14-dev libgdbm-compat4t64
18.82   libgnutls30t64 libgomp1 libgprofng0 libgssapi-krb5-2 libhwasan0 libidn2-0
18.82   libisl23 libitm1 libjansson4 libk5crypto3 libkeyutils1 libkrb5-3
18.82   libkrb5support0 libldap-common libldap2 liblocale-gettext-perl liblsan0
18.82   libmpc3 libmpfr6 libnghttp2-14 libnghttp3-9 libngtcp2-16
18.82   libngtcp2-crypto-gnutls8 libp11-kit0 libperl5.40 libpsl5t64 libquadmath0
18.82   librtmp1 libsasl2-2 libsasl2-modules libsasl2-modules-db libsframe1
18.82   libssh2-1t64 libstdc++-14-dev libtasn1-6 libtsan2 libubsan1 libunistring5
18.82   libx11-6 libx11-data libxau6 libxcb1 libxdmcp6 libxext6 libxmuu1
18.82   linux-libc-dev make manpages manpages-dev openssh-client patch perl
18.82   perl-modules-5.40 publicsuffix rpcsvc-proto sq wget xauth xz-utils
19.33 0 upgraded, 107 newly installed, 0 to remove and 0 not upgraded.
19.33 Need to get 112 MB of archives.
19.33 After this operation, 449 MB of additional disk space will be used.
19.33 Get:1 http://deb.debian.org/debian trixie/main amd64 libexpat1 amd64 2.7.1-2 [108 kB]
19.52 Get:2 http://deb.debian.org/debian trixie/main amd64 liblocale-gettext-perl amd64 1.07-7+b1 [15.3 kB]
19.91 Get:3 http://deb.debian.org/debian trixie/main amd64 less amd64 668-1 [161 kB]
20.21 Get:4 http://deb.debian.org/debian trixie/main amd64 bzip2 amd64 1.0.8-6 [40.5 kB]
20.46 Get:5 http://deb.debian.org/debian trixie/main amd64 krb5-locales all 1.21.3-5 [101 kB]
24.42 Get:6 http://deb.debian.org/debian trixie/main amd64 manpages all 6.9.1-1 [1393 kB]
24.91 Get:7 http://deb.debian.org/debian trixie/main amd64 libedit2 amd64 3.1-20250104-1 [93.8 kB]
25.18 Get:8 http://deb.debian.org/debian trixie/main amd64 libcbor0.10 amd64 0.10.2-2 [28.3 kB]
25.32 Get:9 http://deb.debian.org/debian trixie/main amd64 libfido2-1 amd64 1.15.0-1+b1 [78.7 kB]
25.52 Get:10 http://deb.debian.org/debian trixie/main amd64 libkrb5support0 amd64 1.21.3-5 [33.0 kB]
25.70 Get:11 http://deb.debian.org/debian trixie/main amd64 libcom-err2 amd64 1.47.2-3+b3 [25.0 kB]
25.86 Get:12 http://deb.debian.org/debian trixie/main amd64 libk5crypto3 amd64 1.21.3-5 [81.5 kB]
26.00 Get:13 http://deb.debian.org/debian trixie/main amd64 libkeyutils1 amd64 1.6.3-6 [9456 B]
26.32 Get:14 http://deb.debian.org/debian trixie/main amd64 libkrb5-3 amd64 1.21.3-5 [326 kB]
26.58 Get:15 http://deb.debian.org/debian trixie/main amd64 libgssapi-krb5-2 amd64 1.21.3-5 [138 kB]
27.42 Get:16 http://deb.debian.org/debian trixie/main amd64 openssh-client amd64 1:10.0p1-7 [985 kB]
27.60 Get:17 http://deb.debian.org/debian trixie/main amd64 perl-modules-5.40 all 5.40.1-6 [3019 kB]
28.22 Get:18 http://deb.debian.org/debian trixie/main amd64 libgdbm-compat4t64 amd64 1.24-2 [50.3 kB]
28.31 Get:19 http://deb.debian.org/debian trixie/main amd64 libperl5.40 amd64 5.40.1-6 [4341 kB]
30.06 Get:20 http://deb.debian.org/debian trixie/main amd64 perl amd64 5.40.1-6 [267 kB]
30.45 Get:21 http://deb.debian.org/debian trixie/main amd64 libunistring5 amd64 1.3-2 [477 kB]
30.73 Get:22 http://deb.debian.org/debian trixie/main amd64 libidn2-0 amd64 2.3.8-2 [109 kB]
31.20 Get:23 http://deb.debian.org/debian trixie/main amd64 libp11-kit0 amd64 0.25.5-3 [425 kB]
31.41 Get:24 http://deb.debian.org/debian trixie/main amd64 libtasn1-6 amd64 4.20.0-2 [49.9 kB]
32.18 Get:25 http://deb.debian.org/debian trixie/main amd64 libgnutls30t64 amd64 3.8.9-3 [1465 kB]
32.53 Get:26 http://deb.debian.org/debian trixie/main amd64 libpsl5t64 amd64 0.21.2-1.1+b1 [57.2 kB]
37.13 Get:27 http://deb.debian.org/debian trixie/main amd64 wget amd64 1.25.0-2 [984 kB]
38.60 Get:28 http://deb.debian.org/debian trixie/main amd64 xz-utils amd64 5.8.1-1 [660 kB]
38.99 Get:29 http://deb.debian.org/debian trixie/main amd64 libsframe1 amd64 2.44-3 [78.4 kB]
39.10 Get:30 http://deb.debian.org/debian trixie/main amd64 binutils-common amd64 2.44-3 [2509 kB]
40.05 Get:31 http://deb.debian.org/debian trixie/main amd64 libbinutils amd64 2.44-3 [534 kB]
40.48 Get:32 http://deb.debian.org/debian trixie/main amd64 libgprofng0 amd64 2.44-3 [808 kB]
40.83 Get:33 http://deb.debian.org/debian trixie/main amd64 libctf-nobfd0 amd64 2.44-3 [156 kB]
41.02 Get:34 http://deb.debian.org/debian trixie/main amd64 libctf0 amd64 2.44-3 [88.6 kB]
41.23 Get:35 http://deb.debian.org/debian trixie/main amd64 libjansson4 amd64 2.14-2+b3 [39.8 kB]
43.10 Get:36 http://deb.debian.org/debian trixie/main amd64 binutils-x86-64-linux-gnu amd64 2.44-3 [1014 kB]
44.21 Get:37 http://deb.debian.org/debian trixie/main amd64 binutils amd64 2.44-3 [265 kB]
44.50 Get:38 http://deb.debian.org/debian trixie/main amd64 libc-dev-bin amd64 2.41-12 [58.2 kB]
44.59 Get:39 http://deb.debian.org/debian trixie/main amd64 linux-libc-dev all 6.12.57-1 [2692 kB]
46.52 Get:40 http://deb.debian.org/debian trixie/main amd64 libcrypt-dev amd64 1:4.4.38-1 [119 kB]
46.93 Get:41 http://deb.debian.org/debian trixie/main amd64 rpcsvc-proto amd64 1.4.3-1 [63.3 kB]
47.00 Get:42 http://deb.debian.org/debian trixie/main amd64 libc6-dev amd64 2.41-12 [1991 kB]
47.79 Get:43 http://deb.debian.org/debian trixie/main amd64 libisl23 amd64 0.27-1 [659 kB]
48.48 Get:44 http://deb.debian.org/debian trixie/main amd64 libmpfr6 amd64 4.2.2-1 [729 kB]
48.86 Get:45 http://deb.debian.org/debian trixie/main amd64 libmpc3 amd64 1.3.1-1+b3 [52.2 kB]
48.97 Get:46 http://deb.debian.org/debian trixie/main amd64 cpp-14-x86-64-linux-gnu amd64 14.2.0-19 [11.0 MB]
51.54 Get:47 http://deb.debian.org/debian trixie/main amd64 cpp-14 amd64 14.2.0-19 [1280 B]
51.68 Get:48 http://deb.debian.org/debian trixie/main amd64 cpp-x86-64-linux-gnu amd64 4:14.2.0-1 [4840 B]
81.99 Ign:49 http://deb.debian.org/debian trixie/main amd64 cpp amd64 4:14.2.0-1
81.99 Ign:50 http://deb.debian.org/debian trixie/main amd64 libcc1-0 amd64 14.2.0-19
81.99 Ign:51 http://deb.debian.org/debian trixie/main amd64 libgomp1 amd64 14.2.0-19
81.99 Ign:52 http://deb.debian.org/debian trixie/main amd64 libitm1 amd64 14.2.0-19
81.99 Ign:53 http://deb.debian.org/debian trixie/main amd64 libatomic1 amd64 14.2.0-19
81.99 Ign:54 http://deb.debian.org/debian trixie/main amd64 libasan8 amd64 14.2.0-19
81.99 Ign:55 http://deb.debian.org/debian trixie/main amd64 liblsan0 amd64 14.2.0-19
81.99 Ign:56 http://deb.debian.org/debian trixie/main amd64 libtsan2 amd64 14.2.0-19
81.99 Ign:57 http://deb.debian.org/debian trixie/main amd64 libubsan1 amd64 14.2.0-19
81.99 Ign:58 http://deb.debian.org/debian trixie/main amd64 libhwasan0 amd64 14.2.0-19
81.99 Ign:59 http://deb.debian.org/debian trixie/main amd64 libquadmath0 amd64 14.2.0-19
82.99 Ign:59 http://deb.debian.org/debian trixie/main amd64 libquadmath0 amd64 14.2.0-19
82.99 Ign:58 http://deb.debian.org/debian trixie/main amd64 libhwasan0 amd64 14.2.0-19
82.99 Ign:57 http://deb.debian.org/debian trixie/main amd64 libubsan1 amd64 14.2.0-19
82.99 Ign:56 http://deb.debian.org/debian trixie/main amd64 libtsan2 amd64 14.2.0-19
82.99 Ign:55 http://deb.debian.org/debian trixie/main amd64 liblsan0 amd64 14.2.0-19
82.99 Ign:54 http://deb.debian.org/debian trixie/main amd64 libasan8 amd64 14.2.0-19
82.99 Ign:53 http://deb.debian.org/debian trixie/main amd64 libatomic1 amd64 14.2.0-19
82.99 Ign:52 http://deb.debian.org/debian trixie/main amd64 libitm1 amd64 14.2.0-19
82.99 Ign:51 http://deb.debian.org/debian trixie/main amd64 libgomp1 amd64 14.2.0-19
82.99 Ign:50 http://deb.debian.org/debian trixie/main amd64 libcc1-0 amd64 14.2.0-19
82.99 Ign:49 http://deb.debian.org/debian trixie/main amd64 cpp amd64 4:14.2.0-1
85.00 Ign:49 http://deb.debian.org/debian trixie/main amd64 cpp amd64 4:14.2.0-1
85.00 Ign:50 http://deb.debian.org/debian trixie/main amd64 libcc1-0 amd64 14.2.0-19
85.00 Ign:51 http://deb.debian.org/debian trixie/main amd64 libgomp1 amd64 14.2.0-19
85.00 Ign:52 http://deb.debian.org/debian trixie/main amd64 libitm1 amd64 14.2.0-19
85.00 Ign:53 http://deb.debian.org/debian trixie/main amd64 libatomic1 amd64 14.2.0-19
85.00 Ign:54 http://deb.debian.org/debian trixie/main amd64 libasan8 amd64 14.2.0-19
85.00 Ign:55 http://deb.debian.org/debian trixie/main amd64 liblsan0 amd64 14.2.0-19
85.00 Ign:56 http://deb.debian.org/debian trixie/main amd64 libtsan2 amd64 14.2.0-19
85.00 Ign:57 http://deb.debian.org/debian trixie/main amd64 libubsan1 amd64 14.2.0-19
85.00 Ign:58 http://deb.debian.org/debian trixie/main amd64 libhwasan0 amd64 14.2.0-19
85.00 Ign:59 http://deb.debian.org/debian trixie/main amd64 libquadmath0 amd64 14.2.0-19
89.00 Err:59 http://deb.debian.org/debian trixie/main amd64 libquadmath0 amd64 14.2.0-19
89.00   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
89.00 Err:58 http://deb.debian.org/debian trixie/main amd64 libhwasan0 amd64 14.2.0-19
89.00   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
89.00 Err:57 http://deb.debian.org/debian trixie/main amd64 libubsan1 amd64 14.2.0-19
89.00   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
89.00 Err:56 http://deb.debian.org/debian trixie/main amd64 libtsan2 amd64 14.2.0-19
89.00   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
89.00 Err:55 http://deb.debian.org/debian trixie/main amd64 liblsan0 amd64 14.2.0-19
89.00   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
89.00 Err:54 http://deb.debian.org/debian trixie/main amd64 libasan8 amd64 14.2.0-19
89.00   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
89.00 Err:53 http://deb.debian.org/debian trixie/main amd64 libatomic1 amd64 14.2.0-19
89.00   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
89.00 Err:52 http://deb.debian.org/debian trixie/main amd64 libitm1 amd64 14.2.0-19
89.00   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
89.00 Err:51 http://deb.debian.org/debian trixie/main amd64 libgomp1 amd64 14.2.0-19
89.00   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
89.00 Err:50 http://deb.debian.org/debian trixie/main amd64 libcc1-0 amd64 14.2.0-19
89.00   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
89.00 Err:49 http://deb.debian.org/debian trixie/main amd64 cpp amd64 4:14.2.0-1
89.00   Could not connect to debian.map.fastlydns.net:80 (199.232.170.132), connection timed out Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
89.00   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
89.00 Ign:60 http://deb.debian.org/debian trixie/main amd64 libgcc-14-dev amd64 14.2.0-19
89.00 Ign:61 http://deb.debian.org/debian trixie/main amd64 gcc-14-x86-64-linux-gnu amd64 14.2.0-19
89.00 Ign:62 http://deb.debian.org/debian trixie/main amd64 gcc-14 amd64 14.2.0-19
89.00 Ign:63 http://deb.debian.org/debian trixie/main amd64 gcc-x86-64-linux-gnu amd64 4:14.2.0-1
89.00 Ign:64 http://deb.debian.org/debian trixie/main amd64 gcc amd64 4:14.2.0-1
89.00 Ign:65 http://deb.debian.org/debian trixie/main amd64 libstdc++-14-dev amd64 14.2.0-19
89.00 Ign:66 http://deb.debian.org/debian trixie/main amd64 g++-14-x86-64-linux-gnu amd64 14.2.0-19
89.00 Ign:67 http://deb.debian.org/debian trixie/main amd64 g++-14 amd64 14.2.0-19
89.00 Ign:68 http://deb.debian.org/debian trixie/main amd64 g++-x86-64-linux-gnu amd64 4:14.2.0-1
89.00 Ign:69 http://deb.debian.org/debian trixie/main amd64 g++ amd64 4:14.2.0-1
89.00 Ign:70 http://deb.debian.org/debian trixie/main amd64 make amd64 4.4.1-2
90.00 Ign:70 http://deb.debian.org/debian trixie/main amd64 make amd64 4.4.1-2
90.00 Ign:69 http://deb.debian.org/debian trixie/main amd64 g++ amd64 4:14.2.0-1
90.00 Ign:68 http://deb.debian.org/debian trixie/main amd64 g++-x86-64-linux-gnu amd64 4:14.2.0-1
90.00 Ign:67 http://deb.debian.org/debian trixie/main amd64 g++-14 amd64 14.2.0-19
90.00 Ign:66 http://deb.debian.org/debian trixie/main amd64 g++-14-x86-64-linux-gnu amd64 14.2.0-19
90.01 Ign:65 http://deb.debian.org/debian trixie/main amd64 libstdc++-14-dev amd64 14.2.0-19
90.01 Ign:64 http://deb.debian.org/debian trixie/main amd64 gcc amd64 4:14.2.0-1
90.01 Ign:63 http://deb.debian.org/debian trixie/main amd64 gcc-x86-64-linux-gnu amd64 4:14.2.0-1
90.01 Ign:62 http://deb.debian.org/debian trixie/main amd64 gcc-14 amd64 14.2.0-19
90.01 Ign:61 http://deb.debian.org/debian trixie/main amd64 gcc-14-x86-64-linux-gnu amd64 14.2.0-19
90.01 Ign:60 http://deb.debian.org/debian trixie/main amd64 libgcc-14-dev amd64 14.2.0-19
92.04 Ign:60 http://deb.debian.org/debian trixie/main amd64 libgcc-14-dev amd64 14.2.0-19
92.04 Ign:61 http://deb.debian.org/debian trixie/main amd64 gcc-14-x86-64-linux-gnu amd64 14.2.0-19
92.04 Ign:62 http://deb.debian.org/debian trixie/main amd64 gcc-14 amd64 14.2.0-19
92.04 Ign:63 http://deb.debian.org/debian trixie/main amd64 gcc-x86-64-linux-gnu amd64 4:14.2.0-1
92.04 Ign:64 http://deb.debian.org/debian trixie/main amd64 gcc amd64 4:14.2.0-1
92.04 Ign:65 http://deb.debian.org/debian trixie/main amd64 libstdc++-14-dev amd64 14.2.0-19
92.04 Ign:66 http://deb.debian.org/debian trixie/main amd64 g++-14-x86-64-linux-gnu amd64 14.2.0-19
92.04 Ign:67 http://deb.debian.org/debian trixie/main amd64 g++-14 amd64 14.2.0-19
92.04 Ign:68 http://deb.debian.org/debian trixie/main amd64 g++-x86-64-linux-gnu amd64 4:14.2.0-1
92.04 Ign:69 http://deb.debian.org/debian trixie/main amd64 g++ amd64 4:14.2.0-1
92.04 Ign:70 http://deb.debian.org/debian trixie/main amd64 make amd64 4.4.1-2
96.04 Err:70 http://deb.debian.org/debian trixie/main amd64 make amd64 4.4.1-2
96.04   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
96.04 Err:69 http://deb.debian.org/debian trixie/main amd64 g++ amd64 4:14.2.0-1
96.04   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
96.04 Err:68 http://deb.debian.org/debian trixie/main amd64 g++-x86-64-linux-gnu amd64 4:14.2.0-1
96.04   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
96.04 Err:67 http://deb.debian.org/debian trixie/main amd64 g++-14 amd64 14.2.0-19
96.04   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
96.04 Err:66 http://deb.debian.org/debian trixie/main amd64 g++-14-x86-64-linux-gnu amd64 14.2.0-19
96.04   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
96.04 Err:65 http://deb.debian.org/debian trixie/main amd64 libstdc++-14-dev amd64 14.2.0-19
96.04   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
96.04 Err:64 http://deb.debian.org/debian trixie/main amd64 gcc amd64 4:14.2.0-1
96.04   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
96.04 Err:63 http://deb.debian.org/debian trixie/main amd64 gcc-x86-64-linux-gnu amd64 4:14.2.0-1
96.04   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
96.04 Err:62 http://deb.debian.org/debian trixie/main amd64 gcc-14 amd64 14.2.0-19
96.04   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
96.04 Err:61 http://deb.debian.org/debian trixie/main amd64 gcc-14-x86-64-linux-gnu amd64 14.2.0-19
96.04   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
96.04 Err:60 http://deb.debian.org/debian trixie/main amd64 libgcc-14-dev amd64 14.2.0-19
96.04   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
96.04 Ign:71 http://deb.debian.org/debian trixie/main amd64 libdpkg-perl all 1.22.21
96.04 Ign:72 http://deb.debian.org/debian trixie/main amd64 patch amd64 2.8-2
96.04 Ign:73 http://deb.debian.org/debian trixie/main amd64 dpkg-dev all 1.22.21
96.04 Ign:74 http://deb.debian.org/debian trixie/main amd64 build-essential amd64 12.12
96.04 Ign:75 http://deb.debian.org/debian trixie/main amd64 libfakeroot amd64 1.37.1.1-1
96.04 Ign:76 http://deb.debian.org/debian trixie/main amd64 fakeroot amd64 1.37.1.1-1
96.04 Ign:77 http://deb.debian.org/debian trixie/main amd64 libbrotli1 amd64 1.1.0-2+b7
96.04 Ign:78 http://deb.debian.org/debian trixie/main amd64 libsasl2-modules-db amd64 2.1.28+dfsg1-9
96.04 Ign:79 http://deb.debian.org/debian trixie/main amd64 libsasl2-2 amd64 2.1.28+dfsg1-9
96.04 Ign:80 http://deb.debian.org/debian trixie/main amd64 libldap2 amd64 2.6.10+dfsg-1
96.04 Ign:81 http://deb.debian.org/debian trixie/main amd64 libnghttp2-14 amd64 1.64.0-1.1
97.04 Ign:81 http://deb.debian.org/debian trixie/main amd64 libnghttp2-14 amd64 1.64.0-1.1
97.04 Ign:80 http://deb.debian.org/debian trixie/main amd64 libldap2 amd64 2.6.10+dfsg-1
97.05 Ign:79 http://deb.debian.org/debian trixie/main amd64 libsasl2-2 amd64 2.1.28+dfsg1-9
97.05 Ign:78 http://deb.debian.org/debian trixie/main amd64 libsasl2-modules-db amd64 2.1.28+dfsg1-9
97.05 Ign:77 http://deb.debian.org/debian trixie/main amd64 libbrotli1 amd64 1.1.0-2+b7
97.05 Ign:76 http://deb.debian.org/debian trixie/main amd64 fakeroot amd64 1.37.1.1-1
97.05 Ign:75 http://deb.debian.org/debian trixie/main amd64 libfakeroot amd64 1.37.1.1-1
97.05 Ign:74 http://deb.debian.org/debian trixie/main amd64 build-essential amd64 12.12
97.05 Ign:73 http://deb.debian.org/debian trixie/main amd64 dpkg-dev all 1.22.21
97.05 Ign:72 http://deb.debian.org/debian trixie/main amd64 patch amd64 2.8-2
97.05 Ign:71 http://deb.debian.org/debian trixie/main amd64 libdpkg-perl all 1.22.21
99.05 Ign:71 http://deb.debian.org/debian trixie/main amd64 libdpkg-perl all 1.22.21
99.05 Ign:72 http://deb.debian.org/debian trixie/main amd64 patch amd64 2.8-2
99.05 Ign:73 http://deb.debian.org/debian trixie/main amd64 dpkg-dev all 1.22.21
99.05 Ign:74 http://deb.debian.org/debian trixie/main amd64 build-essential amd64 12.12
99.05 Ign:75 http://deb.debian.org/debian trixie/main amd64 libfakeroot amd64 1.37.1.1-1
99.05 Ign:76 http://deb.debian.org/debian trixie/main amd64 fakeroot amd64 1.37.1.1-1
99.05 Ign:77 http://deb.debian.org/debian trixie/main amd64 libbrotli1 amd64 1.1.0-2+b7
99.05 Ign:78 http://deb.debian.org/debian trixie/main amd64 libsasl2-modules-db amd64 2.1.28+dfsg1-9
99.05 Ign:79 http://deb.debian.org/debian trixie/main amd64 libsasl2-2 amd64 2.1.28+dfsg1-9
99.05 Ign:80 http://deb.debian.org/debian trixie/main amd64 libldap2 amd64 2.6.10+dfsg-1
99.05 Ign:81 http://deb.debian.org/debian trixie/main amd64 libnghttp2-14 amd64 1.64.0-1.1
103.1 Err:81 http://deb.debian.org/debian trixie/main amd64 libnghttp2-14 amd64 1.64.0-1.1
103.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
103.1 Err:80 http://deb.debian.org/debian trixie/main amd64 libldap2 amd64 2.6.10+dfsg-1
103.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
103.1 Err:79 http://deb.debian.org/debian trixie/main amd64 libsasl2-2 amd64 2.1.28+dfsg1-9
103.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
103.1 Err:78 http://deb.debian.org/debian trixie/main amd64 libsasl2-modules-db amd64 2.1.28+dfsg1-9
103.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
103.1 Err:77 http://deb.debian.org/debian trixie/main amd64 libbrotli1 amd64 1.1.0-2+b7
103.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
103.1 Err:76 http://deb.debian.org/debian trixie/main amd64 fakeroot amd64 1.37.1.1-1
103.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
103.1 Err:75 http://deb.debian.org/debian trixie/main amd64 libfakeroot amd64 1.37.1.1-1
103.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
103.1 Err:74 http://deb.debian.org/debian trixie/main amd64 build-essential amd64 12.12
103.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
103.1 Err:73 http://deb.debian.org/debian trixie/main amd64 dpkg-dev all 1.22.21
103.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
103.1 Err:72 http://deb.debian.org/debian trixie/main amd64 patch amd64 2.8-2
103.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
103.1 Err:71 http://deb.debian.org/debian trixie/main amd64 libdpkg-perl all 1.22.21
103.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
103.1 Ign:82 http://deb.debian.org/debian trixie/main amd64 libnghttp3-9 amd64 1.8.0-1
103.1 Ign:83 http://deb.debian.org/debian trixie/main amd64 libngtcp2-16 amd64 1.11.0-1
103.1 Ign:84 http://deb.debian.org/debian trixie/main amd64 libngtcp2-crypto-gnutls8 amd64 1.11.0-1
103.1 Ign:85 http://deb.debian.org/debian trixie/main amd64 librtmp1 amd64 2.4+20151223.gitfa8646d.1-2+b5
103.1 Ign:86 http://deb.debian.org/debian trixie/main amd64 libssh2-1t64 amd64 1.11.1-1
103.1 Ign:87 http://deb.debian.org/debian trixie/main amd64 libcurl3t64-gnutls amd64 8.14.1-2+deb13u2
103.1 Ign:88 http://deb.debian.org/debian trixie/main amd64 liberror-perl all 0.17030-1
103.1 Ign:89 http://deb.debian.org/debian trixie/main amd64 git-man all 1:2.47.3-0+deb13u1
103.1 Ign:90 http://deb.debian.org/debian trixie/main amd64 git amd64 1:2.47.3-0+deb13u1
103.1 Ign:91 http://deb.debian.org/debian trixie/main amd64 libalgorithm-diff-perl all 1.201-1
103.1 Ign:92 http://deb.debian.org/debian trixie/main amd64 libalgorithm-diff-xs-perl amd64 0.04-9
104.1 Ign:92 http://deb.debian.org/debian trixie/main amd64 libalgorithm-diff-xs-perl amd64 0.04-9
104.1 Ign:91 http://deb.debian.org/debian trixie/main amd64 libalgorithm-diff-perl all 1.201-1
104.1 Ign:90 http://deb.debian.org/debian trixie/main amd64 git amd64 1:2.47.3-0+deb13u1
104.1 Ign:89 http://deb.debian.org/debian trixie/main amd64 git-man all 1:2.47.3-0+deb13u1
104.1 Ign:88 http://deb.debian.org/debian trixie/main amd64 liberror-perl all 0.17030-1
104.1 Ign:87 http://deb.debian.org/debian trixie/main amd64 libcurl3t64-gnutls amd64 8.14.1-2+deb13u2
104.1 Ign:86 http://deb.debian.org/debian trixie/main amd64 libssh2-1t64 amd64 1.11.1-1
104.1 Ign:85 http://deb.debian.org/debian trixie/main amd64 librtmp1 amd64 2.4+20151223.gitfa8646d.1-2+b5
104.1 Ign:84 http://deb.debian.org/debian trixie/main amd64 libngtcp2-crypto-gnutls8 amd64 1.11.0-1
104.1 Ign:83 http://deb.debian.org/debian trixie/main amd64 libngtcp2-16 amd64 1.11.0-1
104.1 Ign:82 http://deb.debian.org/debian trixie/main amd64 libnghttp3-9 amd64 1.8.0-1
106.1 Ign:82 http://deb.debian.org/debian trixie/main amd64 libnghttp3-9 amd64 1.8.0-1
106.1 Ign:83 http://deb.debian.org/debian trixie/main amd64 libngtcp2-16 amd64 1.11.0-1
106.1 Ign:84 http://deb.debian.org/debian trixie/main amd64 libngtcp2-crypto-gnutls8 amd64 1.11.0-1
106.1 Ign:85 http://deb.debian.org/debian trixie/main amd64 librtmp1 amd64 2.4+20151223.gitfa8646d.1-2+b5
106.1 Ign:86 http://deb.debian.org/debian trixie/main amd64 libssh2-1t64 amd64 1.11.1-1
106.1 Ign:87 http://deb.debian.org/debian trixie/main amd64 libcurl3t64-gnutls amd64 8.14.1-2+deb13u2
106.1 Ign:88 http://deb.debian.org/debian trixie/main amd64 liberror-perl all 0.17030-1
106.1 Ign:89 http://deb.debian.org/debian trixie/main amd64 git-man all 1:2.47.3-0+deb13u1
106.1 Ign:90 http://deb.debian.org/debian trixie/main amd64 git amd64 1:2.47.3-0+deb13u1
106.1 Ign:91 http://deb.debian.org/debian trixie/main amd64 libalgorithm-diff-perl all 1.201-1
106.1 Ign:92 http://deb.debian.org/debian trixie/main amd64 libalgorithm-diff-xs-perl amd64 0.04-9
110.1 Err:92 http://deb.debian.org/debian trixie/main amd64 libalgorithm-diff-xs-perl amd64 0.04-9
110.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
110.1 Err:91 http://deb.debian.org/debian trixie/main amd64 libalgorithm-diff-perl all 1.201-1
110.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
110.1 Err:90 http://deb.debian.org/debian trixie/main amd64 git amd64 1:2.47.3-0+deb13u1
110.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
110.1 Err:89 http://deb.debian.org/debian trixie/main amd64 git-man all 1:2.47.3-0+deb13u1
110.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
110.1 Err:88 http://deb.debian.org/debian trixie/main amd64 liberror-perl all 0.17030-1
110.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
110.1 Err:87 http://deb.debian.org/debian trixie/main amd64 libcurl3t64-gnutls amd64 8.14.1-2+deb13u2
110.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
110.1 Err:86 http://deb.debian.org/debian trixie/main amd64 libssh2-1t64 amd64 1.11.1-1
110.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
110.1 Err:85 http://deb.debian.org/debian trixie/main amd64 librtmp1 amd64 2.4+20151223.gitfa8646d.1-2+b5
110.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
110.1 Err:84 http://deb.debian.org/debian trixie/main amd64 libngtcp2-crypto-gnutls8 amd64 1.11.0-1
110.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
110.1 Err:83 http://deb.debian.org/debian trixie/main amd64 libngtcp2-16 amd64 1.11.0-1
110.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
110.1 Err:82 http://deb.debian.org/debian trixie/main amd64 libnghttp3-9 amd64 1.8.0-1
110.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
110.1 Ign:93 http://deb.debian.org/debian trixie/main amd64 libalgorithm-merge-perl all 0.08-5
110.1 Ign:94 http://deb.debian.org/debian trixie/main amd64 libfile-fcntllock-perl amd64 0.22-4+b4
110.1 Ign:95 http://deb.debian.org/debian trixie/main amd64 libldap-common all 2.6.10+dfsg-1
110.1 Ign:96 http://deb.debian.org/debian trixie/main amd64 libsasl2-modules amd64 2.1.28+dfsg1-9
110.1 Ign:97 http://deb.debian.org/debian trixie/main amd64 libxau6 amd64 1:1.0.11-1
110.1 Ign:98 http://deb.debian.org/debian trixie/main amd64 libxdmcp6 amd64 1:1.1.5-1
110.1 Ign:99 http://deb.debian.org/debian trixie/main amd64 libxcb1 amd64 1.17.0-2+b1
110.1 Ign:100 http://deb.debian.org/debian trixie/main amd64 libx11-data all 2:1.8.12-1
110.1 Ign:101 http://deb.debian.org/debian trixie/main amd64 libx11-6 amd64 2:1.8.12-1
110.1 Ign:102 http://deb.debian.org/debian trixie/main amd64 libxext6 amd64 2:1.3.4-1+b3
110.1 Ign:103 http://deb.debian.org/debian trixie/main amd64 libxmuu1 amd64 2:1.1.3-3+b4
111.1 Ign:103 http://deb.debian.org/debian trixie/main amd64 libxmuu1 amd64 2:1.1.3-3+b4
111.1 Ign:102 http://deb.debian.org/debian trixie/main amd64 libxext6 amd64 2:1.3.4-1+b3
111.1 Ign:101 http://deb.debian.org/debian trixie/main amd64 libx11-6 amd64 2:1.8.12-1
111.1 Ign:100 http://deb.debian.org/debian trixie/main amd64 libx11-data all 2:1.8.12-1
111.1 Ign:99 http://deb.debian.org/debian trixie/main amd64 libxcb1 amd64 1.17.0-2+b1
111.1 Ign:98 http://deb.debian.org/debian trixie/main amd64 libxdmcp6 amd64 1:1.1.5-1
111.1 Ign:97 http://deb.debian.org/debian trixie/main amd64 libxau6 amd64 1:1.0.11-1
111.1 Ign:96 http://deb.debian.org/debian trixie/main amd64 libsasl2-modules amd64 2.1.28+dfsg1-9
111.1 Ign:95 http://deb.debian.org/debian trixie/main amd64 libldap-common all 2.6.10+dfsg-1
111.1 Ign:94 http://deb.debian.org/debian trixie/main amd64 libfile-fcntllock-perl amd64 0.22-4+b4
111.1 Ign:93 http://deb.debian.org/debian trixie/main amd64 libalgorithm-merge-perl all 0.08-5
113.1 Ign:93 http://deb.debian.org/debian trixie/main amd64 libalgorithm-merge-perl all 0.08-5
113.1 Ign:94 http://deb.debian.org/debian trixie/main amd64 libfile-fcntllock-perl amd64 0.22-4+b4
113.1 Ign:95 http://deb.debian.org/debian trixie/main amd64 libldap-common all 2.6.10+dfsg-1
113.1 Ign:96 http://deb.debian.org/debian trixie/main amd64 libsasl2-modules amd64 2.1.28+dfsg1-9
113.1 Ign:97 http://deb.debian.org/debian trixie/main amd64 libxau6 amd64 1:1.0.11-1
113.1 Ign:98 http://deb.debian.org/debian trixie/main amd64 libxdmcp6 amd64 1:1.1.5-1
113.1 Ign:99 http://deb.debian.org/debian trixie/main amd64 libxcb1 amd64 1.17.0-2+b1
113.1 Ign:100 http://deb.debian.org/debian trixie/main amd64 libx11-data all 2:1.8.12-1
113.1 Ign:101 http://deb.debian.org/debian trixie/main amd64 libx11-6 amd64 2:1.8.12-1
113.1 Ign:102 http://deb.debian.org/debian trixie/main amd64 libxext6 amd64 2:1.3.4-1+b3
113.1 Ign:103 http://deb.debian.org/debian trixie/main amd64 libxmuu1 amd64 2:1.1.3-3+b4
117.1 Err:103 http://deb.debian.org/debian trixie/main amd64 libxmuu1 amd64 2:1.1.3-3+b4
117.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
117.1 Err:102 http://deb.debian.org/debian trixie/main amd64 libxext6 amd64 2:1.3.4-1+b3
117.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
117.1 Err:101 http://deb.debian.org/debian trixie/main amd64 libx11-6 amd64 2:1.8.12-1
117.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
117.1 Err:100 http://deb.debian.org/debian trixie/main amd64 libx11-data all 2:1.8.12-1
117.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
117.1 Err:99 http://deb.debian.org/debian trixie/main amd64 libxcb1 amd64 1.17.0-2+b1
117.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
117.1 Err:98 http://deb.debian.org/debian trixie/main amd64 libxdmcp6 amd64 1:1.1.5-1
117.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
117.1 Err:97 http://deb.debian.org/debian trixie/main amd64 libxau6 amd64 1:1.0.11-1
117.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
117.1 Err:96 http://deb.debian.org/debian trixie/main amd64 libsasl2-modules amd64 2.1.28+dfsg1-9
117.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
117.1 Err:95 http://deb.debian.org/debian trixie/main amd64 libldap-common all 2.6.10+dfsg-1
117.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
117.1 Err:94 http://deb.debian.org/debian trixie/main amd64 libfile-fcntllock-perl amd64 0.22-4+b4
117.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
117.1 Err:93 http://deb.debian.org/debian trixie/main amd64 libalgorithm-merge-perl all 0.08-5
117.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
117.1 Ign:104 http://deb.debian.org/debian trixie/main amd64 manpages-dev all 6.9.1-1
117.1 Ign:105 http://deb.debian.org/debian trixie/main amd64 publicsuffix all 20250328.1952-0.1
117.1 Ign:106 http://deb.debian.org/debian trixie/main amd64 sq amd64 1.3.1-2+b1
117.1 Ign:107 http://deb.debian.org/debian trixie/main amd64 xauth amd64 1:1.1.2-1.1
118.1 Ign:107 http://deb.debian.org/debian trixie/main amd64 xauth amd64 1:1.1.2-1.1
118.1 Ign:106 http://deb.debian.org/debian trixie/main amd64 sq amd64 1.3.1-2+b1
118.1 Ign:105 http://deb.debian.org/debian trixie/main amd64 publicsuffix all 20250328.1952-0.1
118.1 Ign:104 http://deb.debian.org/debian trixie/main amd64 manpages-dev all 6.9.1-1
120.1 Ign:104 http://deb.debian.org/debian trixie/main amd64 manpages-dev all 6.9.1-1
120.1 Ign:105 http://deb.debian.org/debian trixie/main amd64 publicsuffix all 20250328.1952-0.1
120.1 Ign:106 http://deb.debian.org/debian trixie/main amd64 sq amd64 1.3.1-2+b1
120.1 Ign:107 http://deb.debian.org/debian trixie/main amd64 xauth amd64 1:1.1.2-1.1
124.1 Err:107 http://deb.debian.org/debian trixie/main amd64 xauth amd64 1:1.1.2-1.1
124.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 Err:106 http://deb.debian.org/debian trixie/main amd64 sq amd64 1.3.1-2+b1
124.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 Err:105 http://deb.debian.org/debian trixie/main amd64 publicsuffix all 20250328.1952-0.1
124.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 Err:104 http://deb.debian.org/debian trixie/main amd64 manpages-dev all 6.9.1-1
124.1   Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 Fetched 38.4 MB in 1min 45s (365 kB/s)
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-defaults/cpp_14.2.0-1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-14/libcc1-0_14.2.0-19_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-14/libgomp1_14.2.0-19_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-14/libitm1_14.2.0-19_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-14/libatomic1_14.2.0-19_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-14/libasan8_14.2.0-19_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-14/liblsan0_14.2.0-19_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-14/libtsan2_14.2.0-19_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-14/libubsan1_14.2.0-19_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-14/libhwasan0_14.2.0-19_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-14/libquadmath0_14.2.0-19_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-14/libgcc-14-dev_14.2.0-19_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-14/gcc-14-x86-64-linux-gnu_14.2.0-19_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-14/gcc-14_14.2.0-19_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-defaults/gcc-x86-64-linux-gnu_14.2.0-1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-defaults/gcc_14.2.0-1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-14/libstdc%2b%2b-14-dev_14.2.0-19_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-14/g%2b%2b-14-x86-64-linux-gnu_14.2.0-19_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-14/g%2b%2b-14_14.2.0-19_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-defaults/g%2b%2b-x86-64-linux-gnu_14.2.0-1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/gcc-defaults/g%2b%2b_14.2.0-1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/m/make-dfsg/make_4.4.1-2_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/d/dpkg/libdpkg-perl_1.22.21_all.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/p/patch/patch_2.8-2_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/d/dpkg/dpkg-dev_1.22.21_all.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/b/build-essential/build-essential_12.12_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/f/fakeroot/libfakeroot_1.37.1.1-1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/f/fakeroot/fakeroot_1.37.1.1-1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/b/brotli/libbrotli1_1.1.0-2%2bb7_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/c/cyrus-sasl2/libsasl2-modules-db_2.1.28%2bdfsg1-9_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/c/cyrus-sasl2/libsasl2-2_2.1.28%2bdfsg1-9_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/o/openldap/libldap2_2.6.10%2bdfsg-1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/n/nghttp2/libnghttp2-14_1.64.0-1.1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/n/nghttp3/libnghttp3-9_1.8.0-1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/n/ngtcp2/libngtcp2-16_1.11.0-1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/n/ngtcp2/libngtcp2-crypto-gnutls8_1.11.0-1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/r/rtmpdump/librtmp1_2.4%2b20151223.gitfa8646d.1-2%2bb5_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/libs/libssh2/libssh2-1t64_1.11.1-1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/c/curl/libcurl3t64-gnutls_8.14.1-2%2bdeb13u2_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/libe/liberror-perl/liberror-perl_0.17030-1_all.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/git/git-man_2.47.3-0%2bdeb13u1_all.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/g/git/git_2.47.3-0%2bdeb13u1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/liba/libalgorithm-diff-perl/libalgorithm-diff-perl_1.201-1_all.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/liba/libalgorithm-diff-xs-perl/libalgorithm-diff-xs-perl_0.04-9_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/liba/libalgorithm-merge-perl/libalgorithm-merge-perl_0.08-5_all.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/libf/libfile-fcntllock-perl/libfile-fcntllock-perl_0.22-4%2bb4_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/o/openldap/libldap-common_2.6.10%2bdfsg-1_all.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/c/cyrus-sasl2/libsasl2-modules_2.1.28%2bdfsg1-9_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/libx/libxau/libxau6_1.0.11-1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/libx/libxdmcp/libxdmcp6_1.1.5-1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/libx/libxcb/libxcb1_1.17.0-2%2bb1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/libx/libx11/libx11-data_1.8.12-1_all.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/libx/libx11/libx11-6_1.8.12-1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/libx/libxext/libxext6_1.3.4-1%2bb3_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/libx/libxmu/libxmuu1_1.1.3-3%2bb4_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/m/manpages/manpages-dev_6.9.1-1_all.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/p/publicsuffix/publicsuffix_20250328.1952-0.1_all.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/r/rust-sequoia-sq/sq_1.3.1-2%2bb1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Failed to fetch http://deb.debian.org/debian/pool/main/x/xauth/xauth_1.1.2-1.1_amd64.deb  Unable to connect to deb.debian.org:http: [IP: 199.232.170.132 80]
124.1 E: Unable to fetch some archives, maybe run apt-get update or try with --fix-missing?
------

 1 warning found (use docker --debug to expand):
 - FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 14)
Dockerfile.prod:20
--------------------
  19 |     # Install system dependencies for building
  20 | >>> RUN apt-get update && apt-get install -y \
  21 | >>>     build-essential \
  22 | >>>     wget \
  23 | >>>     git \
  24 | >>>     && rm -rf /var/lib/apt/lists/*
  25 |
--------------------
ERROR: failed to solve: process "/bin/sh -c apt-get update && apt-get install -y     build-essential     wget     git     && rm -rf /var/lib/apt/lists/*" did not complete successfully: exit code: 100

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/0wbvdgzng56l2z2dpqh9bsstp

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>
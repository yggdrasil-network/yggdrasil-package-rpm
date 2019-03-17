# Yggdrasil RPM

This is a specification file used to build RPMs for Yggdrasil.

## How-to

This assumes you have Go 1.11 or later installed.

Start by installing `rpmbuild`:
```
dnf install rpmbuild
```

Create the working folders:
```
mkdir -p /tmp/rpmbuild/BUILD /tmp/rpmbuild/RPMS /tmp/rpmbuild/SOURCES /tmp/rpmbuild/SPECS /tmp/rpmbuild/SRPMS
```

Place the `yggdrasil.spec` file into `/tmp/rpmbuild/SPECS`.

Download the sources for the specified version, e.g. `v0.3.5`:
```
curl -o/tmp/rpmbuild/SOURCES/v0.3.5 https://codeload.github.com/yggdrasil-network/yggdrasil-go/tar.gz/v0.3.5
```

Build the RPM:
```
cd /tmp/rpmbuild/
rpmbuild -v -bb SPECS/yggdrasil.spec
```

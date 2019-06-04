##
## This SPEC file is for yggdrasil-DEVELOP package and therefore requires 
## special versioning! 
## Version and commit need to be adapted to the latest commit in the yggdrasil develop branch.
## Go into develop branch and run: git describe --tags HEAD 
##      v0.3.5-103-gcab4b5f
## This version string needs to be changes because the "Version" parameter does not allow hyphens! (replace by underscore). Also remove the "v" prefix.
## Don't forget to update the "commit" variable, too! 
## e.g. Version should be: 
##      0.3.5_103_gcab4b5f
##

Name:           yggdrasil-develop
Version:        0.3.5_103_gcab4b5f
%global commit  cab4b5f7934529cad65342a9bf50fef0596b5f2d
Release:        1%{?dist}
Summary:        End-to-end encrypted IPv6 networking. Develop builds.

License:        GPLv3
URL:            https://yggdrasil-network.github.io
Source:         https://github.com/yggdrasil-network/yggdrasil-go/archive/%{commit}.tar.gz

%{?systemd_requires}
BuildRequires:  systemd golang >= 1.11 git
Requires(pre):  shadow-utils
Conflicts:      yggdrasil

%description
Yggdrasil is a proof-of-concept to explore a wholly different approach to
network routing. Whereas current computer networks depend heavily on very
centralised design and configuration, Yggdrasil breaks this mould by making
use of a global spanning tree to form a scalable IPv6 encrypted mesh network.

%pre
getent group yggdrasil >/dev/null || groupadd -r yggdrasil
exit 0

%prep
%setup -qn yggdrasil-go-%{commit}

%build
export PKGSRC="github.com/yggdrasil-network/yggdrasil-go/src/yggdrasil"
export PKGNAME="%{name}"
export PKGVER="%{version}"
./build -t -l "-linkmode=external"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_sysconfdir}/systemd/system
install -m 0755 yggdrasil %{buildroot}/%{_bindir}/yggdrasil
install -m 0755 yggdrasilctl %{buildroot}/%{_bindir}/yggdrasilctl
install -m 0755 contrib/systemd/yggdrasil.service %{buildroot}/%{_sysconfdir}/systemd/system/yggdrasil.service

%files
%{_bindir}/yggdrasil
%{_bindir}/yggdrasilctl
%{_sysconfdir}/systemd/system/yggdrasil.service

%post
%systemd_post yggdrasil.service

%preun
%systemd_preun yggdrasil.service

%postun
%systemd_postun_with_restart yggdrasil.service

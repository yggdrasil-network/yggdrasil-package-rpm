Name:           yggdrasil
Version:        0.5.5
Release:        1%{?dist}
Summary:        End-to-end encrypted IPv6 networking

License:        GPLv3
URL:            https://yggdrasil-network.github.io
Source:         https://codeload.github.com/yggdrasil-network/yggdrasil-go/tar.gz/v%{version}

%{?systemd_requires}
BuildRequires:  systemd golang >= 1.20 git
Requires(pre):  shadow-utils
Conflicts:      yggdrasil-develop

%description
Yggdrasil is a proof-of-concept to explore a wholly different approach to
network routing. Whereas current computer networks depend heavily on very
centralised design and configuration, Yggdrasil breaks this mould by making
use of a global spanning tree to form a scalable IPv6 encrypted mesh network.

%define debug_package %{nil}

%pre
getent group yggdrasil >/dev/null || groupadd -r yggdrasil
exit 0

%prep
%setup -qn yggdrasil-go-%{version}

%build
export PKGNAME="%{name}"
export PKGVER="%{version}"
export GOPROXY="https://proxy.golang.org,direct"
LDFLAGS="" ./build -t -p -l "-linkmode=external"

%install
rm -rf %{buildroot}
install -m 0755 -D yggdrasil %{buildroot}/%{_bindir}/yggdrasil
install -m 0755 -D yggdrasilctl %{buildroot}/%{_bindir}/yggdrasilctl
install -m 0755 -D contrib/systemd/yggdrasil.service %{buildroot}/%{_sysconfdir}/systemd/system/yggdrasil.service

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

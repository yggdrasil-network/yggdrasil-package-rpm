Name:           yggdrasil
Version:        0.3.14
Release:        3
Summary:        End-to-end encrypted IPv6 networking

License:        GPL-3.0-only
Group:          Productivity/Networking/Other
URL:            https://yggdrasil-network.github.io
Source:         v%{version}
Source1:        go.txz

%{?systemd_requires}
BuildRequires:  systemd go >= 1.13 git
Requires(pre):  shadow
Conflicts:      yggdrasil-develop

%description
Yggdrasil is a proof-of-concept to explore a wholly different approach to
network routing. Whereas current computer networks depend heavily on very
centralised design and configuration, Yggdrasil breaks this mould by making
use of a global spanning tree to form a scalable IPv6 encrypted mesh network.

%define debug_package %{nil}

%prep
%setup -qn yggdrasil-go-%{version}

%build

tar xf %SOURCE1
export GOPATH="$(pwd)/go/"
export PKGSRC="github.com/yggdrasil-network/yggdrasil-go/src/yggdrasil"
export PKGNAME="%{name}"
export PKGVER="%{version}"
./build -t -l "-linkmode=external"

%install
rm -rf %{buildroot}
install -m 0755 -D yggdrasil %{buildroot}/%{_bindir}/yggdrasil
install -m 0755 -D yggdrasilctl %{buildroot}/%{_bindir}/yggdrasilctl
install -m 0644 -D contrib/systemd/yggdrasil.service %{buildroot}%{_prefix}/lib/systemd/system/yggdrasil.service

%files
%{_bindir}/yggdrasil
%{_bindir}/yggdrasilctl
%{_prefix}/lib/systemd/system/yggdrasil.service

%pre
getent group yggdrasil >/dev/null || groupadd -r yggdrasil
%service_add_pre yggdrasil.service

%post
%service_add_post yggdrasil.service

%preun
%service_del_preun yggdrasil.service

%postun
%service_del_postun yggdrasil.service

%changelog

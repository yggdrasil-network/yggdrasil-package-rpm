Name:           yggdrasil
Version:        0.3.14
Release:        1%{?dist}
Summary:        End-to-end encrypted IPv6 networking

License:        GPL-3.0-only
Group:          Productivity/Networking/Other
URL:            https://yggdrasil-network.github.io
Source:         https://codeload.github.com/yggdrasil-network/yggdrasil-go/tar.gz/v%{version}

%{?systemd_requires}
BuildRequires:  systemd go >= 1.13 git
Requires(pre):  shadow
Conflicts:      yggdrasil-develop popura popura-develop

%description
Yggdrasil is a proof-of-concept to explore a wholly different approach to
network routing. Whereas current computer networks depend heavily on very
centralised design and configuration, Yggdrasil breaks this mould by making
use of a global spanning tree to form a scalable IPv6 encrypted mesh network.

%define debug_package %{nil}

%prep
%setup -qn yggdrasil-go-%{version}

%build
export PKGNAME="%{name}"
export PKGVER="%{version}"
./build -t -p -l "-linkmode=external"

%install
rm -rf %{buildroot}
install -m 0755 -D yggdrasil %{buildroot}/%{_bindir}/yggdrasil
install -m 0755 -D yggdrasilctl %{buildroot}/%{_bindir}/yggdrasilctl
install -m 0644 -D contrib/systemd/yggdrasil.service %{buildroot}%{_prefix}/lib/systemd/system/yggdrasil.service
mkdir -p %{buildroot}%{_sbindir}
ln -sf service %{buildroot}%{_sbindir}/rcyggdrasil

%files
%{_bindir}/yggdrasil
%{_bindir}/yggdrasilctl
%{_prefix}/lib/systemd/system/yggdrasil.service
%{_sbindir}/rcyggdrasil

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

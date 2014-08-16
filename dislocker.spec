Summary:        Utility to access BitLocker encrypted volumes
Name:           dislocker
Version:        0.3.1
Release:        6.20140423git%{?dist}
License:        GPLv2+
Group:          Applications/System
URL:            https://github.com/Aorimn/dislocker#readme
# When using tarball from released upstream version:
# - (not yet available)
#
# When generating tarball package from upstream git:
# - git clone -b develop git://github.com/Aorimn/dislocker.git dislocker-0.3.1
# - cd dislocker-0.3.1; git checkout a1ff2792291837505f3de9b6e008ddb7bd73260a
# - rm -rf .git; cd ..; tar cvfj dislocker-0.3.1.tar.bz2 dislocker-0.3.1
# - Use the visible date of latest git log entry for %{release} in spec file
Source0:        %{name}-%{version}.tar.bz2
BuildRequires:  polarssl-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Dislocker has been designed to read BitLocker encrypted partitions ("drives")
under a Linux system. The driver used to only read volumes encrypted under a
Microsoft Windows 7 system but is now Microsoft Windows Vista capable and has
the write functionality.

The file name where the BitLocker encrypted partition will be decrypted needs
to be given. This may take a long time, depending on the size of the encrypted
partition. But afterward, once the partition is decrypted, the access to the
NTFS partition will be faster than with FUSE. Another thing to think about is
the size of the disk (same size as the volume that is tried to be decrypted).
Nevertheless, once the partition is decrypted, the file can be mounted as any
NTFS partition.

%package -n fuse-dislocker
Summary:        FUSE-Filesystem to access BitLocker encrypted volumes
Group:          Applications/System
BuildRequires:  fuse-devel

%description -n fuse-dislocker
Dislocker has been designed to read BitLocker encrypted partitions ("drives")
under a Linux system. The driver used to only read volumes encrypted under a
Microsoft Windows 7 system but is now Microsoft Windows Vista capable and has
the write functionality.

A mount point needs to be given to fuse-dislocker. Once keys are decrypted, a
file named 'dislocker-file' appears into this provided mount point. This file
is a virtual NTFS partition, it can be mounted as any NTFS partition and then
reading from it or writing to it is possible.

%prep
%setup -q

%build
cd src
make fuse %{?_smp_mflags} WFLAGS="$RPM_OPT_FLAGS" LDFLAGS="%{?__global_ldflags}"
cp -p %{name} fuse-%{name}
make clean
make file %{?_smp_mflags} WFLAGS="$RPM_OPT_FLAGS" LDFLAGS="%{?__global_ldflags}"
cd ..
for file in *.txt; do mv -f $file ${file%.txt}; done

%install
rm -rf $RPM_BUILD_ROOT
install -D -p -m 755 src/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}
install -D -p -m 644 man/dislocker_man $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1
install -D -p -m 755 src/fuse-%{name} $RPM_BUILD_ROOT%{_bindir}/fuse-%{name}
install -D -p -m 644 man/dislocker_man $RPM_BUILD_ROOT%{_mandir}/man1/fuse-%{name}.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGELOG LICENSE README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files -n fuse-dislocker
%defattr(-,root,root,-)
%doc CHANGELOG LICENSE README
%{_bindir}/fuse-%{name}
%{_mandir}/man1/fuse-%{name}.1*

%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-6.20140423git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 14 2014 Robert Scheck <robert@fedoraproject.org> 0.3.1-5.20140423git
- Rebuild for PolarSSL 1.3.8

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-4.20140423git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 01 2014 Robert Scheck <robert@fedoraproject.org> 0.3.1-3.20140423git
- Rebuild for PolarSSL 1.3.6

* Wed Apr 23 2014 Robert Scheck <robert@fedoraproject.org> 0.3.1-2.20140423git
- Upgrade to GIT 20140423 (#991689 #c15)
- Added %%{?__global_ldflags} for make (#991689 #c16)

* Mon Nov 25 2013 Robert Scheck <robert@fedoraproject.org> 0.3.1-1.20131102git
- Upgrade to GIT 20131102 (#991689 #c8)

* Mon Nov 25 2013 Robert Scheck <robert@fedoraproject.org> 0.2.3-2.20130131git
- Changed PolarSSL patch to support PolarSSL 1.2 and 1.3 (#991689 #c5)
- Added the missing Group tag on fuse-dislocker sub-package (#991689 #c5)

* Wed May 08 2013 Robert Scheck <robert@fedoraproject.org> 0.2.3-1.20130131git
- Upgrade to GIT 20130131
- Initial spec file for Fedora and Red Hat Enterprise Linux

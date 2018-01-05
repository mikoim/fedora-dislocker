Summary:         Utility to access BitLocker encrypted volumes
Name:            dislocker
Version:         0.7.1
Release:         4%{?dist}
License:         GPLv2+
Group:           Applications/System
URL:             https://github.com/Aorimn/dislocker
Source0:         https://github.com/Aorimn/dislocker/archive/v%{version}.tar.gz
Requires:        %{name}-libs%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 7
Requires:        ruby(release), ruby(runtime_executable)
%else
Requires:        %{_bindir}/ruby
%endif
Requires(post):  %{_sbindir}/update-alternatives
Requires(preun): %{_sbindir}/update-alternatives
Provides:        %{_bindir}/%{name}
BuildRequires:   cmake, mbedtls-devel, ruby-devel, %{_bindir}/ruby
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Dislocker has been designed to read BitLocker encrypted partitions ("drives")
under a Linux system. The driver has the capability to read/write partitions
encrypted using Microsoft Windows Vista, 7, 8, 8.1 and 10 (AES-CBC, AES-XTS,
128 or 256 bits, with or without the Elephant diffuser, encrypted partitions);
BitLocker-To-Go encrypted partitions (USB/FAT32 partitions).

The file name where the BitLocker encrypted partition will be decrypted needs
to be given. This may take a long time, depending on the size of the encrypted
partition. But afterward, once the partition is decrypted, the access to the
NTFS partition will be faster than with FUSE. Another thing to think about is
the size of the disk (same size as the volume that is tried to be decrypted).
Nevertheless, once the partition is decrypted, the file can be mounted as any
NTFS partition and won't have any link to the original BitLocker partition.

%package libs
Summary:         Libraries for applications using dislocker
Group:           System Environment/Libraries

%description libs
The dislocker-libs package provides the essential shared libraries for any
dislocker client program or interface.

%package -n fuse-dislocker
Summary:         FUSE filesystem to access BitLocker encrypted volumes
Group:           Applications/System
Provides:        %{_bindir}/%{name}
Provides:        dislocker-fuse = %{version}-%{release}
Provides:        dislocker-fuse%{?_isa} = %{version}-%{release}
Requires:        %{name}-libs%{?_isa} = %{version}-%{release}
Requires(post):  %{_sbindir}/update-alternatives
Requires(preun): %{_sbindir}/update-alternatives
BuildRequires:   fuse-devel

%description -n fuse-dislocker
Dislocker has been designed to read BitLocker encrypted partitions ("drives")
under a Linux system. The driver has the capability to read/write partitions
encrypted using Microsoft Windows Vista, 7, 8, 8.1 and 10 (AES-CBC, AES-XTS,
128 or 256 bits, with or without the Elephant diffuser, encrypted partitions);
BitLocker-To-Go encrypted partitions (USB/FAT32 partitions).

A mount point needs to be given to dislocker-fuse. Once keys are decrypted, a
file named 'dislocker-file' appears into this provided mount point. This file
is a virtual NTFS partition, it can be mounted as any NTFS partition and then
reading from it or writing to it is possible.

%prep
%setup -q

%build
%cmake -D WARN_FLAGS="-Wall -Wno-error -Wextra" .
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove standard symlinks due to alternatives
rm -f $RPM_BUILD_ROOT{%{_bindir}/%{name},%{_mandir}/man1/%{name}.1*}

# Remove symlink, because of missing -devel package
rm -f $RPM_BUILD_ROOT%{_libdir}/libdislocker.so

# Clean up files for later usage in documentation
for file in *.md; do mv -f $file ${file%.md}; done
for file in *.txt; do mv -f $file ${file%.txt}; done

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} %{name} %{_bindir}/%{name}-file 60

%preun
if [ $1 = 0 ]; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}-file
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post -n fuse-dislocker
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} %{name} %{_bindir}/%{name}-fuse 80

%preun -n fuse-dislocker
if [ $1 = 0 ]; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}-fuse
fi

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}-bek
%{_bindir}/%{name}-file
%{_bindir}/%{name}-find
%{_bindir}/%{name}-metadata
%{_mandir}/man1/%{name}-file.1*
%{_mandir}/man1/%{name}-find.1*

%files libs
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGELOG README
%{_libdir}/libdislocker.so.*

%files -n fuse-dislocker
%defattr(-,root,root,-)
%{_bindir}/%{name}-fuse
%{_mandir}/man1/%{name}-fuse.1*

%changelog
* Fri Jan 05 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.7.1-4
- F-28: rebuild for ruby25

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 23 2017 Robert Scheck <robert@fedoraproject.org> 0.7.1-1
- Upgrade to 0.7.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.1-5
- F-26: rebuild for ruby24

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 13 2016 Vít Ondruch <vondruch@redhat.com> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Mon Jan 11 2016 Robert Scheck <robert@fedoraproject.org> 0.5.1-2
- Build ruby extension and ship dislocker-find

* Wed Jan 06 2016 Robert Scheck <robert@fedoraproject.org> 0.5.1-1
- Upgrade to 0.5.1

* Sat Jul 25 2015 Robert Scheck <robert@fedoraproject.org> 0.4.1-5
- Rebuilt for mbed TLS 2.0.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Robert Scheck <robert@fedoraproject.org> 0.4.1-3
- Rebuilt for mbed TLS 1.3.11

* Mon Jun 01 2015 Robert Scheck <robert@fedoraproject.org> 0.4.1-2
- Rebuilt for mbed TLS 1.3.10

* Sat May 30 2015 Robert Scheck <robert@fedoraproject.org> 0.4.1-1
- Upgrade to 0.4.1

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

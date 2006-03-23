%define		zope_subname	psycopgda
Summary:	PostgreSQL database adapter for Zope 3
Summary(pl):	Adapter bazy danych PostgreSQL dla Zope 3
Name:		Zope3-%{zope_subname}
Version:	1.0.0
Release:	1
License:	ZPL 2.1
Group:		Development/Tools
Source0:	http://www.zope.org/Products/Zope3-Packages/psycopgda/%{version}/%{zope_subname}-%{version}.tgz
# Source0-md5:	da55609e4612f2c6d431b00dfa57c369
Patch0:		%{name}-python_ver.patch
URL:		http://www.zope.org/Products/Zope3-Packages/psycopgda/view
BuildRequires:	python
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,postun):	/usr/sbin/installzope3package
Requires(post,postun):	rc-scripts
%pyrequires_eq	python-modules
Requires:	Zope3
Requires:	python-psycopg
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		zope_libdir		/usr/lib/zope3
%define		zope_pyscriptdir	/usr/share/zope3/lib/python

%description
PostgreSQL database adapter for Zope 3.

%description -l pl
Adapter bazy danych PostgreSQL dla Zope 3.

%prep
%setup -q -n %{zope_subname}-%{version}
%patch0 -p1

%build
./configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/zope3

python install.py install \
	--root="$RPM_BUILD_ROOT" \
	--install-purelib="%{zope_pyscriptdir}"

mv $RPM_BUILD_ROOT%{_prefix}/zopeskel $RPM_BUILD_ROOT%{_sysconfdir}/zope3

%py_comp $RPM_BUILD_ROOT%{zope_pyscriptdir}
%py_ocomp $RPM_BUILD_ROOT%{zope_pyscriptdir}

find $RPM_BUILD_ROOT -type f -name "*.py" | xargs rm

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/installzope3package %{zope_subname}
%service -q zope3 restart

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/installzope3package -d %{zope_subname}
	%service -q zope3 restart
fi

%files
%defattr(644,root,root,755)
%{zope_pyscriptdir}
%{_sysconfdir}/zope3/zopeskel%{_sysconfdir}/package-includes/*.zcml

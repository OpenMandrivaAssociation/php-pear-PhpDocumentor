%define         _class          PhpDocumentor
%define		_status		beta
%define		_pearname	%{_class}

%define		_requires_exceptions pear(PEAR/PackageFileManager.php)
%define		_provides_exceptions pear(data/PhpDocumentor\\|pear(PhpDocumentor/scripts

Summary:	%{_pearname} - provides automatic documenting of PHP API directly from source
Name:		php-pear-%{_pearname}
Version:	1.3.1
Release:	%mkrel 2
License:	LGPL
Group:		Development/PHP
URL:		http://pear.php.net/package/PhpDocumentor/
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tar.bz2
Patch0:		PhpDocumentor-html_treemenu_includes_fix.diff
Patch1:		PhpDocumentor-includes_fix.diff
Patch2:		PhpDocumentor-smarty.diff
Requires(post): php-pear
Requires(preun): php-pear
Requires:	apache-mod_php
Requires:	php-pear
Requires:	php-smarty
BuildArch:	noarch
BuildRequires:	dos2unix
BuildRequires:	php-pear
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
The phpDocumentor tool is a standalone auto-documentor similar to
JavaDoc written in PHP. It differs from PHPDoc in that it is MUCH
faster, parses a much wider range of php files, and comes with many
customizations including 11 HTML templates, windows help file CHM
output, PDF output, and XML DocBook peardoc2 output for use with
documenting PEAR. In addition, it can do PHPXref source code
highlighting and linking.

Features (short list):
- output in HTML, PDF (directly), CHM (with windows help compiler),
  XML DocBook
- very fast
- web and command-line interface
- fully customizable output with Smarty-based templates
- recognizes JavaDoc-style documentation with special tags customized
  for PHP 4
- automatic linking, class inheritance diagrams and intelligent
  override
- customizable source code highlighting, with phpxref-style
  cross-referencing
- parses standard README/CHANGELOG/INSTALL/FAQ files and includes them
  directly in documentation
- generates a todo list from @todo tags in source
- generates multiple documentation sets based on @access private,
  @internal and {@internal} tags
- example php files can be placed directly in documentation with
  highlighting and phpxref linking using the @example tag
- linking between external manual and API documentation is possible at
  the sub-section level in all output formats
- easily extended for specific documentation needs with Converter
- full documentation of every feature, manual can be generated
  directly from the source code with "phpdoc -c makedocs" in any format
  desired.
- current manual always available at http://www.phpdoc.org/manual.php
- user .ini files can be used to control output, multiple outputs can
  be generated at once

This class has in PEAR status: %{_status}.

%prep

%setup -q -c
%patch0 -p0
%patch1 -p0
%patch2 -p1

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix -U

# i found no way disabling this silly install check
perl -pi -e "s|md5sum=|blablabla=|g" package.xml

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d

pushd %{_pearname}-%{version}*/
    cp ../package.xml .
    pear install --installroot=%{buildroot} --force --ignore-errors package.xml
popd

install -d %{buildroot}%{_datadir}/pear/packages
install -m0644 package.xml %{buildroot}%{_datadir}/pear/packages/%{_pearname}.xml

# fix cache dir and file list
pushd %{buildroot}%{_datadir}/pear/data/PhpDocumentor/phpDocumentor/Converters
    for i in `find -type d -name 'templates_c' | sed -e 's/^\.\///' | sed -e 's/templates_c//' | sed -e 's/\/$//'`; do
	pushd $i
	    rm -rf templates_c
	    install -d %{buildroot}/var/cache/httpd/%{name}/$i/templates_c
	    ln -snf /var/cache/httpd/%{name}/$i/templates_c templates_c 
	popd
    done
popd

find %{buildroot} -name 'templates_c' | sed -e "s|%{buildroot}||" | sed -e 's/^/%attr(0755,apache,apache) %dir /' > %{name}.filelist

# fix docs
rm -rf docs tests tests.tml
mv %{buildroot}%{_datadir}/pear/tests/PhpDocumentor/Documentation/tests tests
mv %{buildroot}%{_datadir}/pear/docs/PhpDocumentor docs

# put this file in place
mv %{buildroot}%{_bindir}/scripts/makedoc.sh %{buildroot}%{_datadir}/pear/PhpDocumentor/scripts/

# fix apache conf on the fly
cat > apache-%{name}.conf << EOF
php_value include_path '.:%{_datadir}/pear:%{_datadir}/smarty'

Alias /PhpDocumentor "%{_datadir}/pear/data/PhpDocumentor"
<Directory "%{_datadir}/pear/data/PhpDocumentor/">
    Options FollowSymLinks Indexes
    AllowOverride None
    Order Deny,Allow
</Directory>

#Alias /HTML_TreeMenu "%{_datadir}/pear/HTML_TreeMenu"
#<Directory "%{_datadir}/pear/HTML_TreeMenu/">
#    Options FollowSymLinks Indexes
#    AllowOverride None
#    Order Deny,Allow
#</Directory>
EOF

install -m0644  apache-%{name}.conf %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf 

# fix buildroot
find %{buildroot} -type f | xargs perl -pi -e "s|%{buildroot}||"

# fix a README.urpmi file
cat > README.urpmi << EOF

Please set your preferred access policy in the %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf file.

Open up the following URL in your favourite web browser:

http://localhost/PhpDocumentor/
EOF

# cleanup
rm -rf %{buildroot}%{_datadir}/pear/.channels
rm -rf %{buildroot}%{_datadir}/pear/.registry
rm -rf %{buildroot}%{_datadir}/pear/.depdb
rm -rf %{buildroot}%{_datadir}/pear/.depdblock
rm -rf %{buildroot}%{_datadir}/pear/.filemap
rm -rf %{buildroot}%{_datadir}/pear/.lock
rm -rf %{buildroot}%{_datadir}/pear/data/PhpDocumentor/HTML_TreeMenu-*
rm -rf %{buildroot}%{_datadir}/pear/data/PhpDocumentor/Smarty-*
rm -rf %{buildroot}%{_datadir}/pear/data/PhpDocumentor/phpDocumentor/Smarty-*
rm -rf %{buildroot}%{_datadir}/pear/PhpDocumentor/phpDocumentor/Smarty-*
rm -rf %{buildroot}%{_datadir}/pear/PhpDocumentor/HTML_TreeMenu-*
rm -f %{buildroot}/var/cache/pear/*

%post
if [ "$1" = "1" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear install --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi
if [ "$1" = "2" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear upgrade -f --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%preun
if [ "$1" = 0 ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear uninstall --nodeps -r %{_pearname}
	fi
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files -f %{name}.filelist
%defattr(644,root,root,755)
%doc docs/* tests README.urpmi
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf 
%attr(0755,root,root) %{_bindir}/phpdoc
%dir %{_datadir}/pear/%{_class}
%{_datadir}/pear/%{_class}/*
%{_datadir}/pear/packages/%{_pearname}.xml
%{_datadir}/pear/data/PhpDocumentor



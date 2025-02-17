%define     _class          PhpDocumentor
%define		upstream_name	%{_class}
%define __noautoreq /usr/bin/php

Name:		php-pear-%{upstream_name}
Version:	1.4.4
Release:	3
Summary:	Provides automatic documenting of PHP API directly from source

License:	LGPL
Group:		Development/PHP
URL:		https://pear.php.net/package/PhpDocumentor/
Source0:	http://download.pear.php.net/package/%{upstream_name}-%{version}.tgz
Patch:		PhpDocumentor-1.4.3-use-system-smarty.patch
Requires(post): php-pear
Requires(preun): php-pear
Requires:	apache-mod_php
Requires:	php-pear
Requires:	php-smarty
BuildArch:	noarch
BuildRequires:	php-pear

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

%prep
%setup -q -c
# %%patch -p1 <- needs testing
mv package.xml %{upstream_name}-%{version}/%{upstream_name}.xml

%install

cd %{upstream_name}-%{version}
pear install --nodeps --packagingroot %{buildroot} %{upstream_name}.xml
rm -rf %{buildroot}%{_datadir}/pear/.??*

rm -rf %{buildroot}%{_datadir}/pear/docs
rm -rf %{buildroot}%{_datadir}/pear/tests

install -d %{buildroot}%{_datadir}/pear/packages
install -m 644 %{upstream_name}.xml %{buildroot}%{_datadir}/pear/packages

# # cleanup
# rm -rf %{buildroot}%{_datadir}/pear/%{_class}/Smarty-*
# rm -rf %{buildroot}%{_datadir}/pear/%{_class}/phpDocumentor/Smarty-*
# rm -rf %{buildroot}%{_datadir}/pear/data/PhpDocumentor/phpDocumentor/Smarty-*

%clean



%files
%{_bindir}/phpdoc
%{_datadir}/pear/%{_class}
%{_datadir}/pear/data/%{_class}
%{_datadir}/pear/packages/%{upstream_name}.xml



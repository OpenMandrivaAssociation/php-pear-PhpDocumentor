%define     _class          PhpDocumentor
%define		upstream_name	%{_class}

Name:		php-pear-%{upstream_name}
Version:	1.4.4
Release:	2
Summary:	Provides automatic documenting of PHP API directly from source
License:	LGPL
Group:		Development/PHP
URL:		http://pear.php.net/package/PhpDocumentor/
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
%defattr(-,root,root)
%{_bindir}/phpdoc
%{_datadir}/pear/%{_class}
%{_datadir}/pear/data/%{_class}
%{_datadir}/pear/packages/%{upstream_name}.xml


%changelog
* Sun Dec 18 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.4-1mdv2012.0
+ Revision: 743437
- 1.4.4
- fix major breakage by careless packager
- mass rebuild

* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-2mdv2011.0
+ Revision: 613761
- the mass rebuild of 2010.1 packages

* Sat Nov 21 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.3-1mdv2010.1
+ Revision: 468055
- spec cleanup
- use pear installer
- don't ship tests, even in documentation
- own all directories
- use rpm filetriggers starting from mandriva 2010.1

* Sat Sep 26 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.3-1mdv2010.0
+ Revision: 449334
- new version
- use pear installer
- use fedora %%post/%%postun
- update smarty patch

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Raphaël Gertz <rapsys@mandriva.org>
    - New version 1.4.2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-3mdv2009.1
+ Revision: 322656
- rebuild

* Thu Jul 17 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-2mdv2009.0
+ Revision: 237057
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Nov 27 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-1mdv2008.1
+ Revision: 113456
- 1.4.0
- use the default smarty compile dir
- "rediff" the patches

* Mon Apr 23 2007 Oden Eriksson <oeriksson@mandriva.com> 1.3.2-2mdv2008.0
+ Revision: 17259
- fix a silly typo

* Fri Apr 20 2007 Oden Eriksson <oeriksson@mandriva.com> 1.3.2-1mdv2008.0
+ Revision: 15996
- rediffed the patches
- 1.3.2


* Tue Mar 27 2007 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-2mdv2007.1
+ Revision: 148836
- fix #19769

* Sun Nov 12 2006 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-1mdv2007.0
+ Revision: 83419
- 1.3.1
- fix deps
- rediffed patches; P0,P1,P3
- rebuild
- Import php-pear-PhpDocumentor

* Fri Feb 10 2006 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-0.RC5.3mdk
- new group (Development/PHP)

* Mon Jan 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-0.RC5.2mdk
- fix P2 to point to the correct cache directory and also nuke a stray ")"

* Thu Dec 08 2005 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-0.RC5.1mdk
- 1.3.0RC5
- major packaging changes

* Fri Aug 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1.2.2.1-6mdk
- rebuilt to fix auto deps

* Wed Aug 10 2005 Oden Eriksson <oeriksson@mandriva.com> 1.2.2.1-5mdk
- rebuilt to use new pear auto deps/reqs from pld

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 1.2.2.1-4mdk
- fix deps

* Thu Jul 21 2005 Oden Eriksson <oeriksson@mandriva.com> 1.2.2.1-3mdk
- reworked the %%post and %%preun stuff, like in conectiva
- fix deps

* Wed Jul 20 2005 Oden Eriksson <oeriksson@mandriva.com> 1.2.2.1-2mdk
- fix deps

* Tue Jul 19 2005 Oden Eriksson <oeriksson@mandriva.com> 1.2.2.1-1mdk
- initial Mandriva package (PLD import)


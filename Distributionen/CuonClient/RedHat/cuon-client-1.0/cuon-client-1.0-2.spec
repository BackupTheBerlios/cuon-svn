Buildroot: /misc/Projekte/cuon/Distributionen/CuonClient/RedHat/cuon-client-1.0
Name: cuon-client
Version: 1.0
Release: 2
Summary: Installs the cuon client,  
License: see /usr/share/doc/cuon-client/copyright
Distribution: Fedora
Group: python
Requires: python, bash, wget,  python-gtk2,  python-glade2,  python-imaging,   python-gtkmozembed ,  python-gnome2,   python-gtksourceview2 

Packager: Jürgen Hamel <jhamel@cuon.org>
%define _rpmdir ../
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm
%define _unpackaged_files_terminate_build 0

%description
                       using to connect to the cuon server 


%files
%dir "/"
%dir "/usr/"
%dir "/usr/share/"
%dir "/usr/share/pixmaps/"
"/usr/share/pixmaps/cuon-logo.svg"
"/usr/share/pixmaps/cuon-logo.png"
%dir "/usr/share/applications/"
"/usr/share/applications/cuon-client.desktop"
"/usr/share/applications/Client-Config.desktop"
%dir "/usr/bin/"
"/usr/bin/cuon_config_wizard"
"/usr/bin/cuon_client_install"

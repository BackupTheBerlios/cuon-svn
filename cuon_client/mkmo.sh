cd Py
find -name "*.py" > po.files
cd ..

find -name "*.c" >> po.files

xgettext -k_ -kN_ -o messages.pot -f po.files  


msgmerge -U de.po messages.pot


cd cuon
find -name "*.py" > po.files
cd ..
echo "./Cuon.py" >> po.files

find -name "*.c" >> po.files
echo "po.files created"

xgettext -k_ -kN_ -o messages.pot -f po.files  
echo "messages.pot created"

msgmerge -U de.po messages.pot
echo "finish"


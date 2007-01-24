
find cuon/ -name "*.py" > po.files
find cuon/ -name "*.c" >> po.files


echo "./Cuon.py" >> po.files

find GUI/ -name "*.c" >> po.files

echo "`pwd`"
echo "po.files created"
grep -v cuon/bin po.files > p2.files
xgettext -k_ -kN_ -o messages.pot -f po2.files  
echo "messages.pot created"

echo "creating german"
msgmerge -U de.po messages.pot
echo "creating portuguese"
msgmerge -U pt.po messages.pot
echo "creating portuguese_brasilian"
msgmerge -U pt_BR.po messages.pot

echo "finish"


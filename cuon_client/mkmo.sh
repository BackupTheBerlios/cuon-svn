
find cuon/ -name "*.py" > po.files
find cuon/ -name "*.glade2" > po_glade.files


echo "./Cuon.py" >> po.files

find GUI/ -name "*.glade2" >> po_glade.files

echo "`pwd`"
echo "po.files created"
grep -v cuon/bin po.files | grep -v alternate > po2.files
grep -v cuon/bin po_glade.files | grep -v alternate | grep -v 800 | grep -v maemo  > po2_glade.files

xgettext --language=Python -k_ -kN_ -o messages.pot_u1 -f po2.files 
xgettext --language=Glade -k_ -kN_ -o messages_glade.pot -f po2_glade.files
sed 's/'CHARSET'/'utf-8'/g' messages.pot_u1  > messages.pot_u
tail -n +18  messages_glade.pot >> messages.pot_u


echo "messages.pot created"
msguniq --unique messages.pot_u > messages.pot
#cp messages.pot_u  messages.pot

echo "check out on duplicates"

echo "creating german"
cp de.po de_u.po
msguniq de_u.po > de.po

msgmerge -U de.po messages.pot
echo "creating portuguese"
cp pt.po de_u.po
msguniq de_u.po > pt.po
msgmerge -U pt.po messages.pot

echo "creating portuguese_brasilian"
cp pt_BR.po de_u.po
msguniq de_u.po > pt_BR.po
msgmerge -U pt_BR.po messages.pot

echo "creating latvian"
cp lv.po de_u.po
msguniq de_u.po > lv.po
msgmerge -U lv.po messages.pot
echo "creating italian"
cp it.po de_u.po
msguniq de_u.po > it.po
msgmerge -U it.po messages.pot

echo "creating dutch"
cp nl.po de_u.po
msguniq de_u.po > nl.po
msgmerge -U nl.po messages.pot

echo "finish"


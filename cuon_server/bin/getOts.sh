#! /bin/sh
echo "Parameter = $1 $2 $3 $4"

case $1 in 

    txt ) ots -r $2 -o $3 $4.$1 
        ;;
       
    pdf ) pdftotext $4.$1
        ots -r $2 -o $3 $4.txt 
    ;;
    
    odt) odt2text --output=$4.txt $4.$1
     ots -r $2 -o $3 $4.txt 
    ;;
    
    
    
esac


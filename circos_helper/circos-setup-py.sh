# Updated by E St. John
#!/bin/bash
color0=""
color50=""
color70=""
color90=""
scaler=""
scaleq=""
while getopts :R:Q:a:b:c:d:r:q:p:s: opt; do
	case $opt in
		R)
			prodigal -a RE_prot.fasta -i $OPTARG
			grep "^>" RE_prot.fasta | sed 's/>//' | awk '{print $1,$3,$5}' > HASH_ref.txt
			makeblastdb -in RE_prot.fasta -out OUT_DB -dbtype prot
			;;
		Q)
			
			prodigal -a QU_prot.fasta -i $OPTARG
			grep "^>" QU_prot.fasta | sed 's/>//' | awk '{print $1,$3,$5}' > HASH_query.txt
			blastp -query QU_prot.fasta -db OUT_DB -out OUT_CSV.csv -evalue 0.00001 -outfmt 7
# Updated to blast_best.pl
           		./blast_best.pl OUT_CSV.csv OUT_CSV_unique.csv
			awk '{print $1,$2,$3}' OUT_CSV_unique.csv > HASH_ref_query.txt
			;;
		a)
			color0=$OPTARG
			;;
		b)
			color50=$OPTARG
			;;
		c)
			color70=$OPTARG
			;;
		d)
			color90=$OPTARG
			;;
		r)
			cp $OPTARG RE_kar2.txt
			;;
		q)
			cp $OPTARG QU_kar2.txt
			;;
		p)
			scaler=$OPTARG
			;;
		s)
			scaleq=$OPTARG
			;;
	esac
done

awk 'NR==FNR{a[$1]=$2FS$3;b[$1]=$2;next}{print b[$1],$1,$2,$3,a[$1]}' HASH_ref_query.txt HASH_query.txt | awk 'NR==FNR{a[$1]=$2FS$3;next}{print $2,$3,$4,$5,a[$1],$6}' HASH_ref.txt - | sed 's/_/ /g' > hash1.txt

if [ $(wc -l < RE_kar.txt) -eq 1 ]
then
	if [ $(wc -l < QU_kar.txt) -eq 1 ]
	then
		awk '{print "QU0",$4,$5,"RE0",$9,$10,$11}' hash1.txt > hash2.txt
	else
		awk '{print "QU"$2,$4,$5,"RE0",$9,$10,$11}' hash1.txt > hash2.txt
	fi
else
	if [ $(wc -l < QU_kar.txt) -eq 1 ]
	then
		awk '{print "QU0",$4,$5,"RE"$7,$9,$10,$11}' hash1.txt > hash2.txt
	else
		awk '{print "QU"$2,$4,$5,"RE"$7,$9,$10,$11}' hash1.txt > hash2.txt
	fi

fi

awk '{if ($7<50 && $7>0) print $0,"'"$color0"'";else if ($7<70 && $7>=50) print $0,"'"$color50"'";else if ($7<90 && $7>=70) print $0,"'"$color70"'";else if ($7>=90) print $0,"'"$color90"'"}' hash2.txt | sort -t\  -nk7 | awk '{print $7="",$0}' > LINKS.txt

echo "chromosomes_display_default = no" > chromosome.conf
echo -n "chromosomes = " >> chromosome.conf
awk '{print $3}' QU_kar2.txt | tr '\n' ';' >> chromosome.conf
awk '{print $3}' RE_kar2.txt | tr '\n' ';' | sed 's/;$//' >> chromosome.conf
# Updated - added next line
echo "$nl" >> chromosome.conf
echo "chromosome_reverse =" >> chromosome.conf
echo -n "chromosome_radius = " >> chromosome.conf
awk '{print $3}' QU_kar2.txt | tr '\n' '%' | sed 's/%/:1.0r;/g' | sed 's/:1.0r;$/:1.0r/' | tr '\n' ';' >> chromosome.conf
# Updated - added next line
echo -n ";" >> chromosome.conf
awk '{print $3}' RE_kar2.txt | tr '\n' '%' | sed 's/%/:1.0r;/g' | sed 's/:1.0r;$/:1.0r/' >> chromosome.conf
# Updated - added next line
echo "$nl" >> chromosome.conf
echo -n "chromosome_scale = " >> chromosome.conf
awk '{print $3}' QU_kar2.txt | tr '\n' '%' | sed 's/%/='"$scaleq"',/g' | sed 's/='"$scaleq"',$/='"$scaleq"'/' | tr '\n' ',' >> chromosome.conf
# Updated - added next line
echo -n "," >> chromosome.conf
awk '{print $3}' RE_kar2.txt | tr '\n' '%' | sed 's/%/='"$scaler"',/g' | sed 's/='"$scaler"',$/='"$scaler"'/' >> chromosome.conf
# Updated - added next line
echo "$nl" >> chromosome.conf
echo "<<include ./chromosome_order.conf>>" >> chromosome.conf

circos -conf circos.conf

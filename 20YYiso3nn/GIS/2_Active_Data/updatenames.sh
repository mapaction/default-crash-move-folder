for f in **/.gitignore
do
 echo "change $f   to   ${f/.gitignore/enable-empty-dir-in-github.txt}"
 git mv $f ${f/.gitignore/enable-empty-dir-in-github.txt}
done

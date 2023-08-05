#hy2py anarcute/lib.hy > anarcute/lib.py
rm dist/*
python3 setup.py sdist
twine upload dist/*
sh reload.sh
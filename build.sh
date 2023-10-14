python3 -m unittest
if [ $? != 0 ]; then
   echo "Tests failed!"
   exit
fi

python3 setup.py sdist

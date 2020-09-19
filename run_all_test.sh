set -xe
for file in `ls | grep "_test.py"`;
do
    python $file
done

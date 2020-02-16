#!/bin/bash

directory=${JOB_LAUNCHER_DIRECTORY:-/app/tmp}
max=${JOB_LAUNCHER_NUMBER:-50}

echo "Directory $directory"
mkdir -p "$directory"

echo "Creating $max files"

for (( c=1; c<=$max; c++ ))
do
  number=$(( ( RANDOM % 100 )  + 1 ))
  filename="${directory}/job:${number}:process"
  # echo "Creating new file ${filename}"
  touch $filename
done

echo "Files creation complete"

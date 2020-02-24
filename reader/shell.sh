if [ ! -f $pwd/scripts ]; then
  mkdir $pwd/scripts
fi

docker run -it --mount type=bind,source="$(pwd)"/scripts,target=/scripts sc_reader_container:latest /bin/bash

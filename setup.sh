#!/bin/bash


setup_dependancies(){
  pip install -r ./requirements.txt
  # gen python grpc things
  [ -d "./python-grpc" ] ||  mkdir ./python-grpc
  python -m grpc_tools.protoc -I ./rust-grpc/ --python_out=./python-grpc \
          --grpc_python_out=./python-grpc ./rust-grpc/proto/helloworld.proto
  # setup grpc rsqlulte rust server
  cd rust-grpc
  cargo build --bin server
}




if [[ $# == "0" ]]; then 
  echo -e "Usage:";
  echo -e "   --setup,-s\t Sets up dependacies, run that first.";
  echo -e "   --test,-t\t Run unit test"
  echo -e "   --run,-r\t runs Music Ripper"
  echo -e "   --update,-u\t incremntally run music ripper"
else
  for arg in "$@";do
    case "$arg" in
      "--setup" | "-s" )
        setup_dependancies
        ;;
      "--test" | "-t" )
        run_tests
        ;;
      "--run" | "-r" )
        setup_alac
        ;;
      "--update" | "-u" )
        setup_nvim
        ;;
      *)
        echo -e "Usage:";
        echo -e "   --setup,-s\t Sets up dependacies, run that first.";
        echo -e "   --test,-t\t Run unit test"
        echo -e "   --run,-r\t Runs Music Ripper"
        echo -e "   --update,-u\t Incremntally run music ripper"
        exit 0
        ;;
    esac
  done
fi

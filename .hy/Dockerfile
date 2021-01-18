FROM ubuntu
RUN apt-get update --fix-missing && apt-get -y install python3.6 && apt-get clean
RUN apt-get update --fix-missing && apt-get -y install python3-tk && apt-get clean
RUN apt-get update --fix-missing && apt-get -y install python3-pip && apt-get clean
RUN pip3 install grpcio && pip3 install protobuf
RUN mkdir /walk && cd /walk && apt-get update --fix-missing && apt-get -y install git && apt-get clean && git clone --branch master https://github.com/josemibnf/SAT-Walk.git && mv SAT-Walk/* . && rm -rf SAT-Walk && rm -rf .git

FROM pytorch/pytorch:latest

RUN apt-get update && \
	apt-get upgrade -y && \
	pip3 install jupyter && \
	mkdir -p /RUP/pytorch
	
CMD ["/bin/bash","-c","jupyter notebook --notebook-dir=/RUP/pytorch --ip 0.0.0.0 --no-browser --allow-root"]

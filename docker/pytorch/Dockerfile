FROM pytorch/pytorch:latest

RUN apt-get update && \
	apt-get upgrade -y && \
	pip3 install jupyter && \
	mkdir /pytorch
	
CMD ["/bin/bash","-c","jupyter notebook --notebook-dir=/pytorch --ip 0.0.0.0 --no-browser --allow-root"]

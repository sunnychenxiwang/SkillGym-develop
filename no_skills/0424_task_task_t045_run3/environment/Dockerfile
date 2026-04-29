FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y python3 python3-pip 
RUN pip3 install --break-system-packages pymatgen numpy scikit-learn==1.4.2 factor-analyzer
WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages pymatgen

# Input files
COPY 1272701 /root/
COPY SiO2-Cristobalite.cif /root/
COPY SiO2-Quartz-alpha.cif /root/


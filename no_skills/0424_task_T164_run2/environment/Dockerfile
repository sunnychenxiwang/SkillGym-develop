FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y python3 python3-pip 

WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages anndata scikit-learn==1.4.2 factor_analyzer pandas numpy scipy h5py pytest scanpy

# Input files
COPY pbmc3k.h5ad /root/
COPY pbmc3k_2.h5ad /root/
COPY pbmc_10k_protein_v3.h5ad /root/


FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y python3 python3-pip 

WORKDIR /root

# Python dependencies
RUN pip3 install --break-system-packages pypdf pandas openpyxl pytest

# Input files
COPY creditcard.csv /root/
COPY invoice.pdf /root/
COPY invoice_2.pdf /root/
COPY purchases.csv /root/
COPY sample-invoice.pdf /root/
COPY transactions.csv /root/


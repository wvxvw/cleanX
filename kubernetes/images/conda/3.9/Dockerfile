from continuumio/conda-ci-linux-64-python3.9

run apt-get update -y && \
    apt-get install -y \
    libgl1-mesa-dri \
    libgl1-mesa-glx \
    libleptonica-dev \
    tesseract-ocr-all \
    libtesseract-dev &&
    conda config --add channels conda-forge && \
    conda config --add channels anaconda && \
    conda install conda-build pytest pycodestyle

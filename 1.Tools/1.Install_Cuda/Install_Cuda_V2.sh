#!/bin/bash

# Supported version
SUPPORTED_VERSION=("10.0" "11.0" "11.2")

echo "Please specify supported cuda version (${SUPPORTED_VERSION[@]})"
read -p "Your select: " CUDA_VERSION
read -p "Do you want remove previous cuda versions ? (y/n): " MULTIPLE_VERSION

# Check cuda version argument
if [ -z "$CUDA_VERSION" ]
  then
    echo "Please specify cuda version!"
    exit 1
elif [ "$CUDA_VERSION" == "10.0" ]
  then
    echo "Installing cuda $CUDA_VERSION, please wait..."
elif [ "$CUDA_VERSION" == "11.0" ]
  then
    echo "Installing cuda $CUDA_VERSION, please wait..."
elif [ "$CUDA_VERSION" == "11.2" ]
  then
    echo "Installing cuda $CUDA_VERSION, please wait..."
else
    echo "Specify cuda version not supported!"
    exit 1
fi

# Check multiple version argument
if [ "$MULTIPLE_VERSION" == "y" ]
  then
    echo "Removing previous cuda installation..."
    sudo rm /etc/apt/sources.list.d/cuda*
    sudo apt remove --autoremove nvidia-cuda-toolkit
    sudo apt remove --autoremove nvidia-*

    sudo apt-get purge nvidia*
    sudo apt-get autoremove
    sudo apt-get autoclean
    sudo rm -rf /usr/local/cuda*

    sudo apt --purge remove "cublas*" "cuda*"
    sudo apt --purge remove "nvidia*"


    sudo add-apt-repository universe
    sudo apt-get update
    sudo apt-get install build-essential dkms
    sudo apt-get install freeglut3 freeglut3-dev libxi-dev libxmu-dev
else
    echo "Installing cuda version $CUDA_VERSION alongside previous cuda installation... "
fi

cd ~
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-repo-ubuntu1804_10.0.130-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1804_10.0.130-1_amd64.deb
# Add key
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
# sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64 /" | sudo tee /etc/apt/sources.list.d/cuda.list
sudo apt-get update

# Install cuda
echo "Installing cuda $CUDA_VERSION, please wait..."
if [ "$CUDA_VERSION" == "10.0" ]
  then
    sudo apt-get -o Dpkg::Options::="--force-overwrite" install cuda-10-0 cuda-drivers -y
elif [ "$CUDA_VERSION" == "11.0" ]
  then
    sudo apt-get -o Dpkg::Options::="--force-overwrite" install cuda-11-0 cuda-drivers -y
elif [ "$CUDA_VERSION" == "11.2" ]
  then
    sudo apt-get -o Dpkg::Options::="--force-overwrite" install cuda-11-2 cuda-drivers -y
fi


echo "export PATH=/usr/local/cuda-$CUDA_VERSION/bin"'${PATH:+:${PATH}}' >> ~/.bashrc
echo "export LD_LIBRARY_PATH=/usr/local/cuda-$CUDA_VERSION"'/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' >> ~/.bashrc
source ~/.bashrc
sudo ldconfig

# Download cuDNN
if [ "$CUDA_VERSION" == "10.0" ]
  then
    FIELD_ID="1RsruDhHGjU3mbyTuJRTTW8JFmNmffW1A"
    FILE_NAME="cudnn-10.0-linux-x64-v7.6.5.32.tgz"
elif [ "$CUDA_VERSION" == "11.0" ]
  then
    FIELD_ID="1Ol3RGuYpmXzRTKCSHMGJXCRSPAo4jFXG"
    FILE_NAME="cudnn-11.3-linux-x64-v8.2.1.32.tgz"
elif [ "$CUDA_VERSION" == "11.2" ]
  then
    FIELD_ID="1Ol3RGuYpmXzRTKCSHMGJXCRSPAo4jFXG"
    FILE_NAME="cudnn-11.3-linux-x64-v8.2.1.32.tgz"
fi

cd ~/Downloads
URL="https://docs.google.com/uc?export=download&id=$FIELD_ID"
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate $URL -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=$FIELD_ID" -O $FILE_NAME && rm -rf /tmp/cookies.txt

# Decompression cuDNN file and copy
tar -xf $FILE_NAME
sudo cp -R cuda/include/* /usr/local/cuda-$CUDA_VERSION/include
sudo cp -R cuda/lib64/* /usr/local/cuda-$CUDA_VERSION/lib64
cd -

echo "Done!!!"
#mkdir gitRepoEVD
cd gitRepoEVD
# install golang
GOREL=go1.9.3.linux-amd64.tar.gz
wget -q https://dl.google.com/go/$GOREL
tar xfz $GOREL
sudo rm -r /usr/local/go
sudo mv go /usr/local/go
rm -f $GOREL
PATH=$PATH:/usr/local/go/bin
echo 'PATH=$PATH:/usr/local/go/bin' >> /home/$USER/.bashrc

cd ..

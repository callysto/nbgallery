# nbgallery

If we want to set up the notebook gallery from here: https://github.com/nbgallery/nbgallery these are some instructions on how to set that up on RAC. We have also included a file on how to upload a lot of notebooks all at once, that are primarily adapted from this blog post: https://blog.ouseful.info/2019/01/21/bulk-notebook-uploads-to-nbgallery-using-selenium/

## Installing Everything From Scratch 

If you set up a new RAC instance (or presumably, any cloud computing instance) you'll need to install Docker and set a few things up before you can run `nbinder`. Your first step is to install Docker

### Docker Installation 

After you've set up an appropriate instance and accessed it remotely via `ssh`, on that instance you first need to install docker. That can be done with the following steps from your remote machine's terminal:

```bash
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
wget https://download.docker.com/linux/ubuntu/gpg 
sudo apt-key add gpg
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu  $(lsb_release -cs)  stable" 
sudo apt-get update
sudo apt-get install docker-ce
sudo apt install docker-compose
```
Once that completes, you have to add your local user `$USER` to the Docker group so we don't have to use `sudo` all the time (and also so stuff just works without mangling the dockerfiles). This can be done with the following :

```bash
sudo groupadd docker
sudo gpasswd -a $USER docker
# Need to refresh in order to have the changes be reflected
newgrp docker 
```

### `nbgallery` Set Up
Now that docker is installed, we can clone the `nbgallery` repository. 

```
git clone https://github.com/nbgallery/nbgallery.git
```

We also have to set up a few environment variables for the admin account, this can be done with the following

```bash
export NBGALLERY_ADMIN_USER='yourusername'
export NBGALLERY_ADMIN_PASSWORD='yourpassword'
export NBGALLERY_ADMIN_EMAIL='your@email'
```
Now, we can finally launch our docker container:

```
cd nbgallery/
docker-compose up &
```
This takes about five minutes, so walk a way and have a coffee.

At the time of writing there is an error that will prevent you from uploading a notebook, so we will just deal with that now (see this: https://github.com/nbgallery/nbgallery/issues/38)
```shell
docker exec --user root nbgallery_solr_1 chown -R solr:solr /opt/solr/server/solr
docker-compose down
docker-compose up 
```
Once that finishes, you should launch a service on `0.0.0.0:3000` which is where the `nbgallery` lives on your instance. 

### Accessing The Site
To check out the website, you'll need to tunnel in and host it locally which can be done with the following from your **local machine:**
```shell
ssh -N -f -L localhost:9000:0.0.0.0:3000 ubuntu@<ip_of_your_instance>
 ```

From there, go to your local web browser, and go to `localhost:9000` and checkout your fresh gallery without any notebooks.

To upload notebooks, you'll need to log in with what you set up with `NBGALLERY_ADMIN_EMAIL` and `NBGALLERY_ADMIN_PASSWORD` in earlier steps. 


## Populating Everything

The scripts included in this repository will guide you to populate your new gallery with notebooks. 

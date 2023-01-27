## Installing the required software in the VM
Run this first in your SSH session: `sudo apt update && sudo apt -y upgrade`
### Docker:
1. Run `sudo apt install docker.io` to install it.
1. Change your settings so that you can run Docker without `sudo`:
    1. Run `sudo groupadd docker`
    1. Run `sudo gpasswd -a $USER docker`
    1. Log out of your SSH session and log back in (you should also restart your VM instance) .
    1. Run `sudo service docker restart`
    1. Test that Docker can run successfully with `docker run hello-world`
    2. If you want to test something more useful please try `docker run -it ubuntu bash`
### Docker compose:
1. Go to https://github.com/docker/compose/releases and copy the URL for the  `docker-compose-linux-x86_64` binary for its latest version.
    * At the time of writing, the last available version is `v2.11.2` and the URL for it is https://github.com/docker/compose/releases/download/v2.11.2/docker-compose-linux-x86_64
1. Create a folder for binary files for your Linux user:
    1. Create a subfolder `bin` in your home account with `mkdir ~/bin`
    1. Go to the folder with `cd ~/bin`
1. Download the binary file with `wget <compose_url> -O docker-compose`
    * If you forget to add the `-O` option, you can rename the file with `mv <long_filename> docker-compose`
    * Make sure that the `docker-compose` file is in the folder with `ls`
1. Make the binary executable with `chmod +x docker-compose`
    * Check the file with `ls` again; it should now be colored green. You should now be able to run it with `./docker-compose version`
1. Go back to the home folder with `cd ~`
1. Run `nano .bashrc` to modify your path environment variable:
    1. Scroll to the end of the file
    1. Add this line at the end:
       ```bash
        export PATH="${HOME}/bin:${PATH}"
        ```
    1. Press `CTRL` + `o` on your keyboard and press Enter afterwards to save the file.
    1. Press `CTRL` + `x` on your keyboard to exit the Nano editor.
1. Reload the path environment variable with `source .bashrc`
1. You should now be able to run Docker compose from anywhere; test it with `docker-compose version`

### Terraform:
1. Run `curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -`
1. Run `sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"`
1. Run `sudo apt-get update && sudo apt-get install terraform`

### Upload Google service account credentials file to VM instance

1. Copy the file from the local machine using sftp
    1. `sftp <your-hostname>`
    1. `put google-credentials.json`

### Creating an environment variable for the credentials

Create an environment variable called `GOOGLE_APPLICATION_CREDENTIALS` and assign it to the path of your json credentials file (covered on _Create a Service Account_ section), which should be `$HOME/.google/credentials/` . Assuming you're running bash:

1. Open `.bashrc`:
    ```sh
    nano ~/.bashrc
    ```
1. At the end of the file, add the following line:
    ```sh
    export GOOGLE_APPLICATION_CREDENTIALS="<path/to/authkeys>.json"
    ```
1. Exit nano with `Ctrl+X`. Follow the on-screen instructions to save the file and exit.
1. Log out of your current terminal session and log back in, or run `source ~/.bashrc` to activate the environment variable.
1. Refresh the token and verify the authentication with the GCP SDK:
    ```sh
    gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
    ```
### Clone the repo in the VM

Log in to your VM instance and run the following from your `$HOME` folder:

```sh
git clone https://github.com/monometa/SFPD-de-capstone-project
```

### Set up project infrastructure with Terraform

Make sure that the credentials are updated and the environment variable is set up.

1. Go to the `terraform` folder.

1. Open `variables.tf` and edit line 12 under the `variable "region"` block so that it matches your preferred region.

1. Initialize Terraform:
    ```sh
    terraform init
    ```
1. Plan the infrastructure and make sure that you're creating a bucket in Cloud Storage as well as a dataset in BigQuery
    ```sh
    terraform plan
    ```
1. If the plan details are as expected, apply the changes.
    ```sh
    terraform apply
    ```
    
---

[Previous Step](google-cloud.md) | [Next Step](airflow.md)

or

[Back to main README](../README.md)

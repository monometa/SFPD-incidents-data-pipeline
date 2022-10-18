### Create a Service Account
- To create a _Service Account_ go to Google Cloud Platform console and in the left panel select the option **IAM & Admin -> Service Accounts**
- Click on **Create Service Account**
- Define a Service account name and description to help you describe what this service account will do
- Add the following roles:
`BigQuery Admin`
`Storage Admin`
`Storage Object Admin`
`Viewer`

In the Service account dashboard click on **Actions -> Manage keys**
- Click on **Add key -> Create new key**
- Choose key type **JSON** and click on Create
- When saving the file, rename it to `google_credentials.json` and store it in your home folder, in `$HOME/.google/credentials/` .
> ***IMPORTANT***: if you're using a VM as recommended, upload this credentials file to the VM.
You will also need to activate the following APIs:
* https://console.cloud.google.com/apis/library/iam.googleapis.com
* https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com

### Generate a SSH Key

- Create a .ssh directory if you're on a Windows environment
- ```cd .ssh ```
- Run the command changing to the desired **KEY_FILENAME** and **USER** ```ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USER -b 2048```
- A file with the structure **key_filename.pub** is saved into the .ssh folder
- Put the public key in Google Cloud Platform
- Go to Navigation Menu -> Compute Engine -> Metadata
- Print the key using bash command in your environment: ```cat key_filename.pub ```
- Copy the value to GCP and save

### Creating a Virtual Machine on GCP

1. From your project's dashboard, go to _Cloud Compute_ > _VM instance_
1. Create a new instance:
    * Any name of your choosing
    * Pick your favourite region. You can check out the regions [in this link](https://cloud.google.com/about/locations).
        > ***IMPORTANT***: make sure that you use the same region for all of your Google Cloud components.
    * Pick a _E2 series_ instance. A _e2-standard-4_ instance is recommended (4 vCPUs, 16GB RAM)
    * Change the boot disk to _Ubuntu_. The _Ubuntu 20.04 LTS_ version is recommended. Also pick at least 30GB of storage.
    * Leave all other settings on their default value and click on _Create_.

### Set up SSH access to the VM

1. Start your instance from the _VM instances_ dashboard in Google Cloud.
1. Copy the external IP address from the _VM instances_ dashboard.
2. Go to the terminal and type ```ssh -i ~/.ssh/gcp username@external_ip``` where gcp corresponds to the _key_filename_.

### Creating SSH config file

1. Open a terminal
2. Change to the folder .ssh: ```cd .ssh```
3. Create a configuration file: ```touch config```
4. Open the configuration file with your default IDE (in my case is VSCode): ```code config```
5. Insert the following code changing the name, IP address, user and IdentityFile to your own
```
Host <your-hostname>
    Hostname <your-machine-external-ip>
    User <your-user-name>
    IdentityFile <path/to/ssh/key> (e.g. C:/Users/<user-name>/.ssh/gcp)
```
6. Execute the ssh command to connect to the Virtual Machine using alias name
```ssh <your-hostname>```
- **Note**: When you stop the VM instance, the external IP address can change, in that case you have to perform steps 4-6 again updating to the new IP address.

---

[Previous Step](prerequisites.md.md) | [Next Step](infrastructure.md.md)

or

[Back to main README](../README.md)

# Fly.io Postgres Backups

This is a very very simple Django application that does hourly backups of your postgres databases on fly.io.

fly.io only does daily backups which might not be enough for you. This application can help you out with that.

It supports backing up multiple postgres databases from different fly accounts to s3. It uses the Django admin ui for easy configurations.

## Usage
You can deploy this application on fly.io yourself.
```bash
fly auth login
```
Change ```<backups>``` to another name.
```bash
export APP_NAME=<backups>
``` 
Generate the fly.toml file using the template
```bash
envsubst < fly_template.toml >> fly.toml
``` 
Create the app
```bash
fly apps create $APP_NAME
```
Create a volume for the sqlite database
```bash
fly volumes create db --region ams --size 1
```
Set secret key
```bash
fly secrets set SECRET_KEY=$(openssl rand -hex 12)
```
Set fly domain
```bash
fly secrets set FLY_DOMAIN=$APP_NAME.fly.dev
```
Deploy the application to fly
```bash
fly deploy
```
ssh in the machine
```bash
fly ssh console
```
Create a superuser
```bash
python manage.py createsuperuser
```

You can now go to the <app_name>.fly.dev/admin to make the configurations.


## TODOs
Currently, the project only supports the bare minimum of features that i need. If you want to contribute, there are many things that could be improved:

- [ ] More advanced scheduling, currently only does hourly backups for all the databases. We want to be able to control the time between backups per database.
- [ ] Notifications system when backups fail.
- [ ] Add tests. For this we would have to run a fly postgres database.
- [ ] Pause the application when Django admin ui is not used and no backups are made. Right now applications is running 24/7.
- [ ] Add support for more storage providers. Currently only s3 is supported.
- [ ] Add option to spin up a new Postgres database from a made backup. Can be useful when things need to be restored quickly.
- [ ] Automatically delete backups after certain period. I currently have this configured within my s3 bucket.
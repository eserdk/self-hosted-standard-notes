# Self Hosted Standard Notes Configuration

This repository contains configuration needed to deploy self-hosted Standard Notes server.  
Configuration includes automated database backups as well as their encryption and storing to S3
bucket. It also includes Standard Notes automated extensions updater and server.

---

# Acknowledgments

- [standardnotes/standalone](https://github.com/standardnotes/standalone) was used as a base repo
  for standard notes services. Licensed
  under [Apache License 2.0](https://github.com/lobaro/restic-backup-docker/blob/master/LICENSE).
- [lobaro/restic-backup-docker](https://github.com/lobaro/restic-backup-docker) was used as a base
  repo for restic configuration. Licensed
  under [GNU Affero General Public License v3.0](https://github.com/standardnotes/standalone/blob/main/LICENSE.txt)
  .
- [iganeshk/standardnotes-extensions](https://github.com/iganeshk/standardnotes-extensions) was used
  as a base repo for writing `notes-extensions-updater`. Licensed
  under [MIT License](https://github.com/iganeshk/standardnotes-extensions/blob/master/LICENSE).

# Configuration

### MariaDB

Everything should be pretty obvious here. Replace `MYSQL_ROOT_PASSWORD`, `MYSQL_PASSWORD`
and `NOTES_PASSWORD` environment variables.

### MariaDB-Backup

You'd need to adjust how often you need to want backups using the `BACKUP_CRON_JOB` variable.

### Notes-Auth

Replace `JWT_SECRET`, `LEGACY_JWT_SECRET` and `PSEUDO_KEY_PARAMS_KEY` environment variables however
you like and keep them secret.

Replace `ENCRYPTION_SERVER_KEY` with a value generated with `openssl rand -hex 32`.

`DB_PASSWORD` should be the same as `NOTES_PASSWORD` defined above in the `MariaDB` section.

Click [here](https://docs.standardnotes.com/self-hosting/getting-started) for more info.

### Notes-Extensions-Updater

`HOST` is basically `https://notes.<YOUR_DOMAIN>.com`.

`GH_USERNAME` is your github username, `GH_TOKEN` is
your [github personal token](https://github.com/settings/tokens) with `public_repo` permission.

### Notes-Sync

`AUTH_JWT_SECRET` should be the same as `JWT_SECRET` mentioned above in the `Notes-Auth` section.

`DB_PASSWORD` should be the same as `NOTES_PASSWORD` mentioned above in the `MariaDB` section.

Click [here](https://docs.standardnotes.com/self-hosting/getting-started) for more info.

### Restic

You'd need to adjust how often you want to create backups using the `BACKUP_CRON` variable.

`RESTIC_REPOSITORY` is your S3 bucket address.

`RESTIC_PASSWORD` is a password for your snapshots.

`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are your S3 bucket access variables.

Click [here](#https://github.com/Lobaro/restic-backup-docker#environment-variables
) for more info.

# How to use

Once you start the server with `docker compose up -d`, it becomes accessible on 443 port (
https).

To start using extensions, copy the `https://notes.<YOUR_DOMAIN>.com/extensions/index.json` and
paste it to the `Enter Your Extended Activation Code` field in Standard Notes app.

# Notes

### FileSafe

I'm not sure if it's possible to configure extensions that use filesafe in such way, that they use
your self-hosted server, thus I'd ask you to either not use such extensions, or to pay for extended
version to support the team. Those extensions seem to be built on top of
the [standardnotes/filesafe-embed](https://github.com/standardnotes/filesafe-embed) library which
has filesafe server hardcoded
to [standardnotes filesafe relay server](https://filesafe.standardnotes.org).

### Restic

Restic in this version supports only S3 bucket. If you need to use any other storage, please, refer
to the original repo mentioned above.

### Logs

I'd recommend using logrotate to cut/compress/delete logs that are written to file.

# Development

Should you have any questions, suggestions, adjustments, don't hesitate to create a PR.
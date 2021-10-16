# Self Hosted Standard Notes Configuration

This repository contains configuration needed to deploy self-hosted Standard Notes server.

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

# How to use

You'd basically need to:

- change several config parameters, e.g. your domain name in `docker-compose.yml` in labels
  sections;
- create `.env` file in every directory containing `sample.env` and change all the parameters needed
  accordingly, especially those that contain credentials.

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
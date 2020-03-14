# Keep only x GitLab backup in S3 compatible Object Storage

docker-image to keep only x GitLab backup in S3 compatible Object Storage.

This tool will be unnecessary when [GitLab Issue #26246](https://gitlab.com/gitlab-org/gitlab/-/issues/26246) will be closed.

## How to use it

Put this content to `docker-compose.yml` and fill variable env values:

```
version: '3.7'
services:
    clean-gitlab-backup:
        image: stephaneklein/clean-gitlab-backup
        environment:
            START_EVERY_DAY_AT_UTC: '02:00'
            NUMBER_BACKUP_TO_KEEP: 2
            S3_REGION_NAME: 'fr-par'
            S3_ENDPOINT_URL: https://s3.fr-par.scw.cloud
            S3_AWS_ACCESS_KEY_ID: ....
            S3_AWS_SECRET_ACCESS_KEY: ....
            S3_BUCKET_NAME: ...
```

Start it:

```
$ docker-compose up -d
$ docker-compose logs -f
2020-03-14 13:54:08,343 [INFO] clean-gitlab-backup started: Running job Every 1 day at 02:00 UTC
2020-03-14 13:55:00,454 [INFO] Start GitLab old backup cleaning...
2020-03-14 13:55:00,649 [INFO] GitLab old backup clean done
```

## How to contribute

```
$ git clone git@github.com:stephane-klein/clean-gitlab-backup.git
$ cd clean-gitlab-backup
$ docker-compose up -d
$ docker-compose exec clean-gitlab-backup bash
# /src/main.py
```

Now you can update `main.py` file.
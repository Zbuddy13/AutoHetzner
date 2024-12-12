Example Compose:
services:
    autohetzner:
        container_name: hetznerSnapshot
        environment:
            - token='insert token'
            - snapshothistory='insert amount of snapshots to keep'
            - sleep='hours between shapshots'
        volumes:
            - /mnt/drive/appdata/hetznerSnapshot:/data
        restart: unless-stopped
        image: zbuddy19/autohetzner:latest

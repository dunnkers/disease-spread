## Building an image

To build an image for Google Container Registry, run:

`docker build -t eu.gcr.io/sixth-utility-268609/importer`

(use `latest` tag if applicable)

## Pushing

Then push it:

`docker push eu.gcr.io/sixth-utility-268609/importer`

(use `latest` tag if applicable)

-> make sure you are logged into `gcloud`.
curl -XPUT "http://127.0.0.1:5002/exposure?ExposureTime=1%2F4000&ISO=100&Aperture=2"
curl -XGET "http://127.0.0.1:5002/exposure?exposure_id=0"

curl -XPUT "http://127.0.0.1:5002/exposure?ExposureTime=1%2F8000&ISO=100&Aperture=3.5"
curl -XGET "http://127.0.0.1:5002/exposure?exposure_id=1"
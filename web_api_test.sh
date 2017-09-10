curl -XPUT "http://127.0.0.1:5002/exposure?ExposureTime=1%2F4000&ISO=100&Aperture=2"
curl -XGET "http://127.0.0.1:5002/exposure?exposure_id=0"
curl -X GET "http://127.0.0.1:5002/aperture?exposure_id=0"
curl -XGET "http://127.0.0.1:5002/ev_by_id?exposure_id=0"
curl F "Aperture=3.5" "http://127.0.0.1:5002/aperture?exposure_id=0"
curl F "ExposureTime=1%2F2000" "http://127.0.0.1:5002/exposure_time?exposure_id=0"
curl -F "ISO=200" -F "change=et" "http://127.0.0.1:5002/iso?exposure_id=0"
curl -F "ISO=400" -F "change=f_no" "http://127.0.0.1:5002/iso?exposure_id=0"

curl -XGET "http://127.0.0.1:5002/calc_dof?Aperture=2&FocalLength=50&coc=0.030&SubjDist=5"
curl -XGET "http://127.0.0.1:5002/calc_coc?FFFocalLength=35&FocalLength=23"

curl -F 'file=@/media/Kyou/unsorted/WIP/Photos/JP TRIP/2017 Summer/23072017/Export_HIR3075.jpg' http://127.0.0.1:5002/upload_image
curl -XGET "http://127.0.0.1:5002/get_exif?image_id=0"

curl -XPUT "http://127.0.0.1:5002/exposure?ExposureTime=1%2F8000&ISO=100&Aperture=3.5"
curl -XGET "http://127.0.0.1:5002/exposure?exposure_id=1"
# Setting/Retrieving exposure
curl -XPUT "http://127.0.0.1:5002/exposure?ExposureTime=1%2F4000&ISO=100&Aperture=2"
curl -XGET "http://127.0.0.1:5002/exposure?exposure_id=0"
curl -X GET "http://127.0.0.1:5002/aperture?exposure_id=0"
curl -XGET "http://127.0.0.1:5002/ev_by_id?exposure_id=0"

# User define Aperture
curl -F "Aperture=3.5" "http://127.0.0.1:5002/aperture?exposure_id=0"

# User define ExposureTime
curl -F "ExposureTime=1%2F2000" "http://127.0.0.1:5002/exposure_time?exposure_id=0"

# User define ISO
curl -F "ISO=200" -F "change=et" "http://127.0.0.1:5002/iso?exposure_id=0"
curl -F "ISO=400" -F "change=f_no" "http://127.0.0.1:5002/iso?exposure_id=0"

# Manual exposure setting

curl -F "ISO=200" -F "Aperture=2" -F "ExposureTime=1%2F4000" "http://127.0.0.1:5002/manual_exposure?exposure_id=0"

# CALC DOF/COC
curl -XGET "http://127.0.0.1:5002/calc_dof?Aperture=2&FocalLength=50&coc=0.030&SubjDist=5"
curl -XGET "http://127.0.0.1:5002/calc_coc?FFFocalLength=35&FocalLength=23"

# Image upload and exif
curl -F 'file=@/media/Kyou/unsorted/WIP/Photos/JP TRIP/2017 Summer/23072017/Export/_HIR3075.jpg' http://127.0.0.1:5002/upload_image
curl -XGET "http://127.0.0.1:5002/get_exif?image_id=0"

# Recommend style
curl -XGET "http://127.0.0.1:5002/recommend_style?image_id=0"

# Recommend settings without image
curl -XGET "http://127.0.0.1:5002/recommend_settings_wo_image?style=SM&target_ev=10&ff_fl=35&orig_fl=23&model=x100s&sensor_size=APSC&max_aperture=16&min_aperture=2&max_shutter_speed=30&min_shutter_speed=1%2F4000&max_iso=6400&min_iso=100&max_fl=35&min_fl=35&multiplier=1.5"

# Recommend settings with image
curl -XGET "http://127.0.0.1:5002/recommend_settings_w_image?style=SM&image_id=0&ff_fl=35&orig_fl=23&model=x100s&sensor_size=APSC&max_aperture=16&min_aperture=2&max_shutter_speed=30&min_shutter_speed=1%2F4000&max_iso=6400&min_iso=100&max_fl=35&min_fl=35&multiplier=1.5"

# Recommend filter with current and target exposure
curl -XGET "http://127.0.0.1:5002/recommend_filter?exposure_id=0&tExposureTime=1%2F400&tAperture=2&tISO=100&ff_fl=35&orig_fl=23&model=x100s&sensor_size=APSC&max_aperture=16&min_aperture=2&max_shutter_speed=30&min_shutter_speed=1%2F4000&max_iso=6400&min_iso=100&max_fl=35&min_fl=35&multiplier=1.5"

# PUT camera config
curl -XPUT "http://127.0.0.1:5002/camera_config?ff_fl=35&orig_fl=23&model=x100s&sensor_size=APSC&max_aperture=16&min_aperture=2&max_shutter_speed=30&min_shutter_speed=1%2F4000&max_iso=6400&min_iso=100&max_fl=35&min_fl=35&multiplier=1.5"

# Setting/Retrieving exposure
curl -XPUT "http://127.0.0.1:5002/exposure?ExposureTime=1%2F8000&ISO=100&Aperture=3.5"
curl -XGET "http://127.0.0.1:5002/exposure?exposure_id=1"

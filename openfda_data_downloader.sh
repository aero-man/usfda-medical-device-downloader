# /bin/zsh

#---------------------------------------------------------------
# Download medical device data from the openFDA API.
#
# This requires 2 HTTPS/curl requests, since openFDA splits the
# data into 2 zip files.
#
# This is intended to run daily via cron job, since
# the openFDA API updates daily.
#---------------------------------------------------------------

# Starting message
echo "Downloading medical device data from openFDA API..."

# Set directory for downloaded openFDA data
device_data_dir="device-data"

# Prep local files to download openFDA data into (2 files total)
echo "Naming local .zip files..."
timestamp=$(date +%s)
new_filename1="medical_device_data_part1_$timestamp.zip"
new_filename2="medical_device_data_part2_$timestamp.zip"
echo "\t$new_filename1"
echo "\t$new_filename2"

# Get medical device data from openFDA API (2 files total)
echo "Curling openFDA API..."
openfda_api_file1="https://download.open.fda.gov/device/registrationlisting/device-registrationlisting-0001-of-0002.json.zip"
openfda_api_file2="https://download.open.fda.gov/device/registrationlisting/device-registrationlisting-0002-of-0002.json.zip"
curl -o $device_data_dir/$new_filename1 $openfda_api_file1
curl -o $device_data_dir/$new_filename2 $openfda_api_file2

# Delete old openFDA data to avoid interactive overwrite prompts
echo "Deleting old JSON medical device data files..."
echo "\t$device_data_dir/device-registrationlisting-0001-of-0002.json"
echo "\t$device_data_dir/device-registrationlisting-0002-of-0002.json"
rm $device_data_dir/device-registrationlisting-0001-of-0002.json
rm $device_data_dir/device-registrationlisting-0002-of-0002.json

# Unzip openFDA data
echo "Unzipping openFDA .zip files..."
echo "\t$new_filename1"
echo "\t$new_filename2"
cd $device_data_dir
unzip $new_filename1
unzip $new_filename2

# Exit message
echo "Done downloading and unzipping openFDA medical device data files."
echo "Files:"
echo "\t$device_data_dir/device-registrationlisting-0001-of-0002.json"
echo "\t$device_data_dir/device-registrationlisting-0002-of-0002.json"

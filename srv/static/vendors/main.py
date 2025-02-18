import os
import sys
import http.client

print("* VENDORS")

# Get the working directory from the first argument or use the script's directory
path_wd = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.realpath(__file__))
print(path_wd)

# Change to the working directory
os.chdir(path_wd)

# Ensure the 'fonts' directory exists
fonts_dir = os.path.join(path_wd, "fonts")
os.makedirs(fonts_dir, exist_ok=True)

# URL details
host = "fonts.gstatic.com"
path = "/s/dmsans/v15/rP2Fp2ywxg089UriCZa4Hz-D.woff2"

# Download the file
conn = http.client.HTTPSConnection(host)
conn.request("GET", path)
response = conn.getresponse()

if response.status == 200:
    font_path = os.path.join(fonts_dir, "fonts.woff2")
    with open(font_path, "wb") as file:
        file.write(response.read())
    print("Download complete: fonts.woff2")
else:
    print("Failed to download the file, status code:", response.status)

conn.close()
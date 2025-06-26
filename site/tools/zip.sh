
folder_name=$(basename "$PWD")

current_date=$(date +"%Y.%m.%d")

output_zip="${folder_name}_${current_date}.zip"

zip -r "$output_zip" . -x "build/*" ".dart_tool/*" ".git/*" ".idea/*" "$output_zip" "pubspec.lock" "README.md" "tools/*" "android/" "web/" "test/"
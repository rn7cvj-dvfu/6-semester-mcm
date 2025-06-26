#!/bin/bash

sort_yaml() {
    local yaml_file="$1"
    if [ ! -f "$yaml_file" ]; then
        echo "Error: File '$yaml_file' not found!"
        return 1
    fi
    sort -o "$yaml_file" "$yaml_file"
}

sort_yaml "i18n/ru_RU/strings_ru.i18n.yaml"
sort_yaml "i18n/en_US/strings_en.i18n.yaml"
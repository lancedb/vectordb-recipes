#!/bin/bash

js=".js"
txt=".txt"
url='https://storage.googleapis.com/data.yt8m.org/2/j/v/'
url1='https://storage.googleapis.com/data.yt8m.org/2/j/i/'

# Check number of arguments
if [ "$#" -lt 1 ]; then
	echo "Usage: bash downloadcategoryids.sh <number-of-videos-per-category>"
	exit 1
fi

numVideos=$1

# Read all category names from selectedcategories.txt
mapfile -t categories < selectedcategories.txt

mkdir -p category-ids

for name in "${categories[@]}"; do
    if [ "$(uname)" == "Darwin" ]; then
        # Mac OS X platform
        mid=$(grep -E "\t$name \(" youtube8mcategories.txt | grep -o "\".*\"" | sed -n 's/"\(.*\)"/\1/p')
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        # GNU/Linux platform
        mid=$(grep -P "\t$name \(" youtube8mcategories.txt | grep -o "\".*\"" | sed -n 's/"\(.*\)"/\1/p')
    fi
    txtName="${name// /_}$txt"
    mid=$mid$js

    curl -o category-ids/$txtName $url$mid

    if [ "$(uname)" == "Darwin" ]; then
        # Mac OS X platform
        grep -E -oh [a-zA-Z0-9_-]{4} category-ids/$txtName > category-ids/tmp$txtName
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        # GNU/Linux platform
        grep -P -oh [a-zA-Z0-9_-]{4} category-ids/$txtName > category-ids/tmp$txtName
    fi

    # First line is not tf-record-id
    tail -n +2 category-ids/tmp$txtName > category-ids/$txtName

    # Just keep as many tf-record-ids as necessary
    if [ "$1" -eq 0 ]; then
        mv category-ids/$txtName category-ids/tmp$txtName
    else
        awk -v var="$numVideos" ' NR <= var' category-ids/$txtName > category-ids/tmp$txtName
    fi

    # Get first two characters of tf-record
    cut -c1-2 category-ids/tmp$txtName > category-ids/tmp2$txtName

    rm -rf category-ids/$txtName

    # Generate the url to fetch-youtube id in category-ids/$txtName
    exec 6<"category-ids/tmp2$txtName"
    while read -r line
    do
        read -r firstTwoChars <&6
        echo "${url1}${firstTwoChars}/${line}.js" >> category-ids/$txtName
    done <"category-ids/tmp${txtName}"
    exec 6<&-

    # Download actual youtube-video-id for each tf-record-id
    rm -rf category-ids/tmp$txtName
    while IFS= read -r line
    do
        if [ "$(uname)" == "Darwin" ]; then
            # Mac OS X platform
            curl "$line" | grep -E -oh [a-zA-Z0-9_-]{11} >> category-ids/tmp$txtName
        elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
            # GNU/Linux platform
            curl "$line" | grep -P -oh [a-zA-Z0-9_-]{11} >> category-ids/tmp$txtName
        fi
    done < category-ids/$txtName

    # Cleanup
    mv category-ids/tmp$txtName category-ids/$txtName
    rm -rf category-ids/tmp$txtName
    rm -rf category-ids/tmp2$txtName

    echo "Completed downloading youtube video-ids for category: $name"
done

# Combine all category video IDs into all.txt
cat category-ids/*.txt > category-ids/all.txt

echo "Completed downloading youtube video-ids for all categories"

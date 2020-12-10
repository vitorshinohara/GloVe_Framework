mkdir -p Dataset
FILE=$1

if [[ $FILE != "Books" && $FILE != "Eletronics" && $FILE != "Movies_and_TV" && $FILE != "CDs_and_Vinyl" && $FILE != "Clothing_Shoes_and_Jewelry" && $FILE != "Home_and_Kitchen" && $FILE != "Kindle_Store" && $FILE != "Sports_and_Outdoors"]]; then
    echo "Available datasets are: Books, Eletronics, Movies_and_TV, CDs_and_Vinyl, Clothing_Shoes_and_Jewelry, Home_and_Kitchen, Kindle_Store, Sports_and_Outdoors"

    Home_and_Kitchen,
    exit 1
fi

echo "Specified [$FILE]"
URL=http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_$FILE_5.json.gz
TARGET_FILE=./Dataset/$FILE.json.gz
OUTPUT_FILE=./Dataset/$FILE.json
TARGET_DIR=./Dataset/$FILE.json.gz
wget -N $URL -O $TARGET_FILE
zcat $TARGET_FILE > $OUTPUT_FILE
rm $TARGET_FILE

mkdir ../../crawled
read -p "Enter a start date: " start
echo "You entered $start"
# echo "$(($start + 1))"
read -p "Enter a end date: " end
echo "You entered $end"
# echo "$(($end + 1))"
for ((i = $start; i <= $end; i++))
do
    echo $i
    wget -P ../../crawled http://data.gdeltproject.org/gkg/$i.gkg.csv.zip
    unzip ../../crawled/$i.gkg.csv.zip -d ../../crawled/
done

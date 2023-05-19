echo "<-------- Running all crawlers --------->"

python3 lockbit_crawler.py >> lockbit_out.log
echo "| ------------ Lockbit crawler done ------------ |"
python3 blackbasta_crawler.py >> black_basta_out.log 
echo "| ------------ Blackbasta crawler done ------------ |"
python3 vice_society_crawler.py >> vice_society_out.log 
echo "| ------------ Vice Society crawler done ------------ |"
python3 bian_lian_crawler.py >> bian_lian_out.log 
echo "| ------------ Bian Lian crawler done ------------ |"
python3 royal_crawler.py >> royal_out.log 
echo "| ------------ Royal crawler done ------------ |"
python3 play_news_crawler.py >> play_news_out.log 
echo "| ------------ Play News crawler done ------------ |"

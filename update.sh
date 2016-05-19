echo "Bygger lista med de senaste tweetsen på disken."
./latesttweet < everything.json > tmp/latest
./split tmp/latest 4
echo "Startar hämtning. Logg skrivs till tmp/stderr.txt"
python3 tweetFetcher.py 1 < tmp/latest.part1 2>> tmp/stderr.txt | gzip -9 > tmp/dump.part1.gz &
python3 tweetFetcher.py 2 < tmp/latest.part2 2>> tmp/stderr.txt | gzip -9 > tmp/dump.part2.gz &
python3 tweetFetcher.py 3 < tmp/latest.part3 2>> tmp/stderr.txt | gzip -9 > tmp/dump.part3.gz &
python3 tweetFetcher.py 4 < tmp/latest.part4 2>> tmp/stderr.txt | gzip -9 > tmp/dump.part4.gz &
wait
echo "Hämtning färdig."
sh process.sh

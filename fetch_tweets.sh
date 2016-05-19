echo "Sorterar user_ids"
sort -u tmp/usr/* > tmp/alluniqeusers
./split tmp/alluniqeusers 4
rm tmp/stderr.txt
echo "Startar hämtning. Logg skrivs till tmp/stderr.txt"
python3 tweetFetcher.py 1 < tmp/alluniqeusers.part1 2>> tmp/stderr.txt | gzip -9 > tmp/dump.part1.gz &
python3 tweetFetcher.py 2 < tmp/alluniqeusers.part2 2>> tmp/stderr.txt | gzip -9 > tmp/dump.part2.gz &
python3 tweetFetcher.py 3 < tmp/alluniqeusers.part3 2>> tmp/stderr.txt | gzip -9 > tmp/dump.part3.gz &
python3 tweetFetcher.py 4 < tmp/alluniqeusers.part4 2>> tmp/stderr.txt | gzip -9 > tmp/dump.part4.gz &
wait
echo "Hämtning färdig."
sh process.sh
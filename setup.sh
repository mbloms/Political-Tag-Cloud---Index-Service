mkdir config
touch config/access.conf

echo '{
    "Moderaterna" : {
        "users" : [
            19226961
        ]
    },
    "Socialdemokraterna": {
        "users": [
            3801501
        ]
    },
    "Vänsterpartiet": {
        "users": [
            17233550
        ]
    },
    "Miljöpartiet": {
        "users": [
            18124359
        ]
    },
    "Sverigedemokraterna": {
        "users": [
            97878686
        ]
    },
    "Liberalerna": {
        "users": [
            18687011
        ]
    },
    "Kristdemokraterna":{
        "users": [
            19014898
        ]
    },
    "Centerpartiet": {
        "users": [
            3796501
        ]
    }
}' > config/accounts.json
ghc -O2 init.hs
ghc -O2 jqprocessor.hs
ghc -O2 latesttweet.hs
ghc -O2 split.hs
echo "Startar hämtning av följare. Vänta.."
./init

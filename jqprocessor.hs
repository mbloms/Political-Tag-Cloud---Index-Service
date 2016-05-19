{-# LANGUAGE DeriveGeneric #-}
import Data.Aeson (FromJSON, ToJSON, eitherDecode)
import Data.Maybe (fromMaybe)
import qualified Data.HashMap.Strict as HM (HashMap, lookup, fromList)
import Data.ByteString.Lazy.UTF8 (fromString, toString)
import qualified Data.Text.Lazy as T
import qualified Data.Text.Lazy.IO as T (readFile, getContents, putStr)
import Data.Text.Lazy.Encoding (encodeUtf8)
import GHC.Generics (Generic)
import Data.List (sort, groupBy)
import qualified Data.List.Utils as LU (merge)
import Prelude hiding (lookup, fromList, fromString, toString, readFile, getContents)
import Data.List (intersperse)
import System.Directory

--Datatyp för átt hämra id och taggar från varje tweet.
data Minimal = Minimal
    { user_id :: T.Text
    , hashtags :: [T.Text]
    } deriving (Show, Generic)

instance FromJSON Minimal
instance ToJSON Minimal

{-
    läser in json-tweeten till listan tweets, delade på radbrytning.
    Skriver ut tweetsen på samma form med "following"-taggen tillagd i början av varje tweet.
    Detta genom att insertPol med rels (hashmapen av relationer) som första argument mappas över alla tweets.
-}
main = do
    input <- T.getContents
    let tweets = T.lines input
    rels <- getRelations
    putLines $ map (insertPol rels) (users tweets)

{-  Hashmap med användare som nykel och poltikerna den följer som element ->
    (user_id,json-tweet) ->
    json-tweet med following-fält tillagt först.
-}
insertPol :: (HM.HashMap T.Text [T.Text]) -> (T.Text,T.Text) -> T.Text
insertPol dict (user,tweet) = T.concat $ p "{\"following\":":following: s ',': T.tail tweet :[]
    where
        following = toText $ fromMaybe [] $ HM.lookup user dict
        p = T.pack
        s = T.singleton

        --funktion som tar en lista av typen [Text] och returnerar den som Text på samma sätt som show.
        toText txts = T.concat $ T.pack "[\"" : intersperse (T.pack "\",\"") txts ++ [T.pack "\"]"]

{-
    Lista av tweets formaterad som json. ->
    Lista av tuples med user_id som första och tweeten oförändrad som andra.
    Tweets utan hashtags filtreras bort.
-}
users :: [T.Text] -> [(T.Text,T.Text)]
users tweets = map minToUser $ filter hasHashtag $ map tuple tweets
    where
        minimal :: T.Text -> Either String Minimal
        minimal tweet = eitherDecode (encodeUtf8 tweet)
        hasHashtag :: (Minimal,a) -> Bool
        hasHashtag (x,_) = not $ (hashtags x) == []
        tuple :: T.Text -> (Minimal, T.Text)
        tuple x =
            if isLeft (minimal x)
                then (Minimal T.empty [], T.concat $ p "{\"error\":\"":p (fromLeft (minimal x)):p "\",":T.tail x:[])
                else (fromRight (minimal x), x)
        minToUser (m,bs) = (user_id m, bs)
        p = T.pack

fromRight (Right a) = a
fromLeft (Left a) = a

isRight :: Either a b -> Bool
isRight (Right _) = True
isRight _ = False
isLeft = not.isRight

{-
    Hämtar alla följare/politiker relationer från mappen tmp och returnerar resultatet som en hashmap.
    Om följaren med id a följer politkern b ligger a på en rad i filen med filnamnet b.
    filinnehållet sorteras och alla filer mergas sen. Detta för att relationerna som hör
    till en följare ska hamna i följd när de slås ihop med compress.
-}
getRelations = do
    files <- listDirectory "tmp"
    let paths = map ("tmp/"++) files
    followers <- fmap (map T.lines) $ mapM T.readFile paths
    --innan zip splittas followers i rader och files packas från String till Text
    let politicians = map T.pack files
    let rels = merge $ map sort $ map (uncurry relations) (zip followers politicians)
    return (HM.fromList $ compress rels)

{-
    Lista av idn som följer -> politiker -> lista med tuples av (alla idn, politikern de följer)
    Ganska självförklarande.
-}
relations :: [T.Text] -> T.Text -> [(T.Text,T.Text)]
relations followers politician = map tuple followers
    where
        tuple :: T.Text -> (T.Text,T.Text)
        tuple follower = (follower, politician)
{-
    Funktion som på samma sätt som merge-sort slår samman redan sorterade listor till en större sorterad.
-}
merge [x] = x
merge lst = merge (mhelper lst)
    where
        mhelper (a:b:cs) = LU.merge a b : mhelper cs
        mhelper lst = lst

{-
    Tar de elementen i listan som har samma första element och slår ihop dem till ett element.
    Andra delen av paret blir då istället en lista med alla (politiker) som den första följer.
-}
compress :: [(T.Text,T.Text)] -> [(T.Text,[T.Text])]
compress relations = map friendlist tuples
    where
        tuples = (groupOn fst . sort) relations
        friendlist lst = ((fst.head) lst,(map snd lst))

        --Mysig funktion som grupperar andra argumentet efter resultatet av första, som är en funktion.
        groupOn :: Eq b => (a -> b) -> [a] -> [[a]]
        groupOn x = groupBy (flip((==).x).x)

putLines a = T.putStr (T.unlines a)
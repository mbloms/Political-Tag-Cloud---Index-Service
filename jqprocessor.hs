{-# LANGUAGE OverloadedStrings, DeriveGeneric #-}
--import Web.Twitter.Types
import Data.Aeson
import Data.Aeson.Types
import Data.Maybe
import qualified Data.HashMap.Strict as HM
import Prelude hiding (lookup, null)
--import Text.JSON
--import Text.DeadSimpleJSON
import qualified Data.ByteString.Lazy.Char8 as BS
import qualified Data.Text as T
import qualified Data.Text.IO as T
import qualified Data.Text.Encoding as T
import GHC.Generics
import Data.List
import qualified Data.List.Utils as LU

jq :: BS.ByteString
jq = "{\"user_id\":\"100004471\",\"tweet_id\":\"361441128958017537\",\"text\":\"RT @FlTNESS: Notice how after you workout you just feel better about yourself?  Keep doing it! #fitness #fitforlife http://t.co/wChySSojhP\",\"hashtags\":[\"fitness\",\"fitforlife\"],\"mentions\":[\"479809444\"],\"lang\":\"en\",\"date\":\"Sun Jul 28 11:00:55 +0000 2013\",\"position\":{\"place\":null,\"geo\":null},\"RT\":{\"retweet_id\":\"361365389751492608\",\"creator_id\":\"479809444\"}}"

{-data Tweet = Tweet
    { user_id :: String
    , tweet_id :: String
    , text :: String
    , hashtags :: [String]
    , mentions :: [String]
    , lang :: String
    , date :: String
    , rt :: RT 
    } deriving (Show, Generic)

instance FromJSON Tweet
instance ToJSON Tweet

data RT = RT
    { retweet_id :: String
    , creator_id :: String
    } deriving (Show, Generic)

instance FromJSON RT
instance ToJSON RT-}

data Minimal = Minimal
    { user_id :: String
    , hashtags :: [String]
    } deriving (Show, Generic)

instance FromJSON Minimal
instance ToJSON Minimal

main = do
    input <- getContents
    let tweets = lines input
    rels <- getRelations
    putLines $ map (insertPol rels) (users tweets)

insertPol :: (HM.HashMap T.Text [T.Text]) -> (String,String) -> String
insertPol dict (user,('{':tweet)) = "{\"following\":"++following++',':tweet
    where
        following = show $ fromMaybe [] $ HM.lookup (T.pack user) dict

users :: [String] -> [(String,String)]
users tweets = map minToUser $ filter (\x->True) $ mapMaybe tuple tweets
    where
        minimal :: String -> Maybe Minimal
        minimal tweet = decode (BS.pack tweet)
        hasHashtag :: (Minimal,a) -> Bool
        hasHashtag (x,_) = not $ (hashtags x) == []
        tuple x =
            if isNothing (minimal x)
                then Nothing
                else Just (fromJust (minimal x), x)
        minToUser (m,bs) = (user_id m, bs)

getRelations = do
    centern <- T.readFile "lek/c.txt"
    kd <- T.readFile "lek/kd.txt"
    liberalerna <- T.readFile "lek/l.txt"
    moderaterna <- T.readFile "lek/moderaterna.txt"
    mp <- T.readFile "lek/mp.txt"
    sd <- T.readFile "lek/sd.txt"
    sossarna <- T.readFile "lek/Socialdemokraterna.txt"
    v <- T.readFile "lek/v.txt"
    let cs = sort $ relations centern 3796501
    let kds = sort $ relations kd 19014898
    let ls = sort $ relations liberalerna 18687011
    let ms = sort $ relations moderaterna 19226961
    let mps = sort $ relations mp 18124359
    let sds = sort $ relations sd 97878686
    let ss = sort $ relations sossarna 3801501
    let vs = sort $ relations v 17233550
    let rels = merge [cs,kds,ls,ms,mps,sds,ss,vs]
    --putLines $ map show $ HM.toList $ HM.fromList $ following rels
    return (HM.fromList $ following rels)


relations :: T.Text -> Integer -> [(T.Text,T.Text)]
relations parti user_id = map tuple followers
    where
        uid = T.pack $ show user_id
        followers :: [T.Text]
        followers = T.lines parti
        tuple :: T.Text -> (T.Text,T.Text)
        tuple follower = (follower, uid)

merge [x] = x
merge lst = merge (mhelper lst)
    where
        mhelper (a:b:cs) = LU.merge a b : mhelper cs
        mhelper lst = lst

maybef _ Nothing = Nothing
maybef f (Just a) = Just (f a)

following :: [(T.Text,T.Text)] -> [(T.Text,[T.Text])]
following relations = map friendlist tuples
    where
        tuples = (groupOn fst . sort) relations
        friendlist lst = ((fst.head) lst,(map snd lst))

groupOn :: Eq b => (a -> b) -> [a] -> [[a]]
groupOn x = groupBy (flip((==).x).x)

--decode $ encode $ toJSON (Hashtag "Hej") :: Maybe Hashtag

nap f a = head $ f [a]

putLines a = putStr (unlines a)
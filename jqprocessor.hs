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

data Minimal = Minimal
    { user_id :: T.Text
    , hashtags :: [T.Text]
    } deriving (Show, Generic)

instance FromJSON Minimal
instance ToJSON Minimal

main = do
    input <- T.getContents
    let tweets = T.lines input
    rels <- getRelations
    putLines $ map (insertPol rels) (users tweets)

insertPol :: (HM.HashMap T.Text [T.Text]) -> (T.Text,T.Text) -> T.Text
insertPol dict (user,tweet) = T.concat $ p "{\"following\":":following: s ',': T.tail tweet :[]
    where
        following = toText $ fromMaybe [] $ HM.lookup user dict
        p = T.pack
        s = T.singleton


toText txts = T.concat $ T.pack "[\"" : intersperse (T.pack "\",\"") txts ++ [T.pack "\"]"]

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

getRelations = do
    files <- listDirectory "tmp"
    let paths = map ("tmp/"++) files
    followers <- mapM T.readFile paths
    let rels = merge $ map sort $ map (uncurry relations) (zip followers (map read files))
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

following :: [(T.Text,T.Text)] -> [(T.Text,[T.Text])]
following relations = map friendlist tuples
    where
        tuples = (groupOn fst . sort) relations
        friendlist lst = ((fst.head) lst,(map snd lst))

        groupOn :: Eq b => (a -> b) -> [a] -> [[a]]
        groupOn x = groupBy (flip((==).x).x)

putLines a = T.putStr (T.unlines a)
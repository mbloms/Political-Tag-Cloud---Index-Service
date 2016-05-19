{-# LANGUAGE DeriveGeneric #-}
import Data.Aeson
import Data.Maybe
import GHC.Generics (Generic)
import qualified Data.ByteString.Lazy.Char8 as BS
import Data.List

--Datatyp för att hämta user och tweet id från varje tweet.
data Minimal = Minimal
    { user_id :: String
    , tweet_id :: String
    } deriving (Show, Generic)

instance FromJSON Minimal
instance ToJSON Minimal

peels :: [Maybe Minimal] -> [(Integer,Integer)]
peels ((Just (Minimal uid tid)):xs) = (read uid,read tid):peels xs
peels (Nothing:xs) = peels xs
peels [] = []

unpeel (uid,tid) = Minimal (show uid) (show tid)

main = do
	dict <- fmap ((map maximum).(groupOn fst).peels.(map decode).BS.lines) BS.getContents
	--mapM_ (BS.putStrLn.encode.unpeel) dict
	mapM_ print dict

groupOn :: Eq b => (a -> b) -> [a] -> [[a]]
groupOn x = groupBy (flip((==).x).x)
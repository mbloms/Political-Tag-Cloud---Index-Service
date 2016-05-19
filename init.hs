{-# LANGUAGE DeriveGeneric #-}
import Data.Aeson
import Data.Maybe
import GHC.Generics (Generic)
import Data.Text (Text)
import qualified Data.ByteString.Lazy.Char8 as BS
import qualified Data.HashMap.Strict as HM

import System.Process
import System.Directory
import Data.Time.Clock.POSIX
import System.Exit

{-
	Läser config-filen och returnerar alla politiker-konton som en IO-lista på Ints.
-}
readPoliticians :: IO [Int]
readPoliticians = do
	conf <- BS.readFile "config/accounts.json"
	return $ concat $ map users $ HM.elems $ fromJust (decode conf :: Maybe Config)

--Datatyper för att avkoda json.
type Config = HM.HashMap Text Users

data Users = Users {users :: [Int]} deriving (Show, Generic)
instance FromJSON Users
instance ToJSON Users

{-
	Tar användar-id som input och startar en följarspya-process som laddar ner alla dess följare
	och sparar dem i filen med samma namn som idt.
	Returnerar en IO ProcessHandle for processen som startats.
-}
fetchFollowers :: Int -> IO ProcessHandle
fetchFollowers uid = spawnCommand $ "echo "++str_id++" | python3 followerFetcher.py > tmp/usr/"++str_id++" 2>>tmp/stderr.txt"
	where str_id = show uid

{-
	Skapar mappen tmp, om den inte finns.
	Hämtar alla politker.
	Startar hämtningar av alla följare.
	Väntar på att hämtningarna ska slutföras.
	Skriver ut mysigt meddelande.
	Copierar filerna till en mapp med tidsstämpel som namn.

	Notera: 
		Kollar inte om något går fel.
		Fel skrivs ut till filen stderr.txt
-}
main = do
	createDirectoryIfMissing True "tmp"
	createDirectoryIfMissing True "tmp/usr"
	politicians <- readPoliticians
	handles <- mapM fetchFollowers politicians
	es <- mapM waitForProcess handles
	case length . filter (/= ExitSuccess) $ es of
            0 -> putStrLn "Fetching followers: Done."
            n -> putStrLn ("There were " ++ show n ++ " failures.")

	timedir <- fmap (("tmp/"++).show.round) getPOSIXTime
	createDirectoryIfMissing True timedir
	renameFile "tmp/stderr.txt" (timedir++"/"++"stderr.txt")
	let backupFile timedir file = copyFile ("tmp/usr/"++file) (timedir++"/"++file)
	mapM_ (backupFile timedir) (map show politicians)
	putStrLn "Files copied."
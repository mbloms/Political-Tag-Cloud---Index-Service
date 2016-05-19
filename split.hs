import System.Environment
import qualified Data.ByteString.Lazy.Char8 as BS

split :: Int -> [a] -> [[a]]
split i lst = map (dropper i) $ map ((flip drop) lst) [0..(i-1)]

dropper :: Int -> [a] -> [a]
dropper i (x:xs) = x: (dropper i $ drop (i-1) xs)
dropper _ [] = []

main = do
	(file:iStr:_) <- getArgs
	let i = read iStr :: Int
	user_ids <- fmap BS.lines $ BS.readFile file
	let parts = map BS.unlines $ split i user_ids
	let files = map ((file++".part")++) (map show [1..i])
	sequence_ $ zipWith BS.writeFile files parts
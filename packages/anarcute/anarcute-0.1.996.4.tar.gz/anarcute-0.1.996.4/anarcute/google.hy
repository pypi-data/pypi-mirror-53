(do (import requests)
    (import [anarcute[*]])
    (require [anarcute.lib[*]])
    
    (defclass GT[object] "Google translate"
      (defn --init-- [self key]
        (setv self.key key
              self.api "https://translation.googleapis.com/language/translate/v2"))
      (defn translate[self source target q &optional [format "text"] [model None]]
        (-> self.api (requests.get  {"key" self.key "q" q "source" source "target" target "format" format "model" model}) (.json))))
    
    (defclass GS[object] "Google Custom Search Engine"
      (defn --init-- [self cx key]
        (setv self.api "https://www.googleapis.com/customsearch/v1/siterestrict")
        (setv self.cx cx self.key key))
      (defn search[self q &optional [follow True][TIMEOUT 10][start 1]]
        (setv res (-> self.api (requests.get :params {"q" q "cx" self.cx "key" self.key "start" start} :timeout TIMEOUT) (.json) )) 
        (if (and (not (in "items" res)) follow (in "spelling" res) (in "correctedQuery" (get res  "spelling")))
          (do (setv corrected (get res "spelling" "correctedQuery"))
              (print "REDIRECT from" q "to" corrected) (self.search corrected :follow True :start start :TIMEOUT TIMEOUT))
          res))
      (defn items[self q &optional [start 1][end None]]
        (setv r (-> q (self.search :start start)))
        (setv items (-> r (get-o "items" []) ))
        (if (and (in "queries" r) (in "nextPage" (get r "queries")) (get r "queries" "nextPage") (or (not end) (< end (len items))))
          (+ items (self.items q :start (get r "queries" "nextPage" 0 "startIndex")))
          items)))
    
   
    
    
    )
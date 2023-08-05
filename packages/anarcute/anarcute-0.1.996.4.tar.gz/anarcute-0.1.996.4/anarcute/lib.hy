(do 
  (import os csv json time sys)
  (require [hy.extra.anaphoric [*]])
  (import [hy.contrib.walk [walk]])
  (import [multiprocessing_on_dill :as mp])
  
  (do "main hall"
      (deftag r[f] `(fn[&rest rest &kwargs kwargs] (~f #*(reversed rest) #**kwargs) ))
      (defn list-dict[arr key] (dict (zip (list (map (fn[x] (get x key)) arr)) arr)))
      (defmacro get-o [&rest args] `(try (get ~@(butlast args)) (except [Exception] ~(last args))))
      (deftag try[expr]`(try ~expr (except [Exception] "")))
      (defn apply-mask[obj mask] (for[(, k v) (.items obj)] (if (in k mask) (assoc obj k ((get mask k) v)))) obj)
      (setv enmask apply-mask)
      (defmacro print-n-pass[x] `(do (print ~x) ~x))
      (defn route[obj &optional[direction None]]
        (setv direction (if direction direction (get-o sys.argv 1 None)))
        (if (in direction obj) ((get obj direction) #*(get sys.argv (slice 2 None))))
        )
      (defn enroute [&rest args]
        (setv compiler (if (.endswith (first sys.argv) ".hy") "hy" "python3"))
        (setv cmd (.format "{} {} {}"  compiler (first sys.argv) (.join " " (list (map (fn[x] (-> x json.dumps)) args)))))
        (os.popen cmd)
        ))
  (do "math"
      (defn avg[&rest args] (if (len args) (/ (+ 0 0 #*args) (len args)) 0))
      (defn roll-avg[&rest args] (cond [(not args) 0] 
                                       [(= 1 (len args)) (if (in (type (first args) )[list tuple]) (roll-avg #*(first args)) (first args))]
                                       [True (+ (* 0.8 (-> args (split-arr 0.8 :from-end True) first roll-avg))
                                                (* 0.2 (-> args (split-arr 0.8 :from-end True) last roll-avg) ))])))
  (do "timey wimey"
      (defn photo-finish-fn [f] (setv start (time.time))
        (setv res (f))
        (, (- (time.time) res)))
      (defmacro photo-finish[&rest args]
        `(do (setv start (time.time))
             ~@args
             (- (time.time) start)
             ))
      (defmacro do-not-faster-than [t &rest args] 
        `(do (setv start (time.time))
             ~@args
             (setv delta (- (time.time) start))
             (if (< 0 delta) (time.sleep (min delta ~t)))))
      (defn timeit[method]
        (defn timed[&rest args &kwargs kwargs]
          (setv ts (time.time)
                result (method #*args #**kwargs)
                te (time.time))
          (if (in "log_time" kwargs)
            (do
              (setv name (kw.get "log_name" (method.__name__.upper)))
              (assoc (get kwargs "log_time") "name" (int (* 1000 (- te ts)))))
            (do (print (% "%r %2.2f ms" (, method.__name__ (* 1000 (- te ts)))))))
          result)
        timed))
  
  (do "common lisp"
      (defmacro car[arr] `(get ~arr 0))
      (defmacro cdr[arr] `(get ~arr (slice 1 None)))
      (defmacro defun[&rest args] `(defn ~@args))
      (defmacro setf[&rest args] `(setv ~@args))
      (defmacro eql[&rest args] `(= ~@(list (map repr args)))))
  (do "anarki/arc")
  (do "pseudo arki"
      `(setv T True
             F False
             N None
             s setv
             c cond
             df defn
             ds defseq))
  (do "predicates"
      (defn in-or[needles haystack] (for [n needles] (if (in n haystack) (return True))) False)
      (defn if?[a b](if a a b))
      
      )
  (do "multithreading"
      (defn mapp[f arr &optional [processes None]]
        (setv processes (if processes processes (mp.cpu-count)))
        (-> processes mp.Pool (.map f arr)))
      (defn filterp[f arr &optional [processes None]]
        (setv verdict (mapp f arr processes))
        (mapp last (list (filter (fn[iv] (get verdict (first iv)) ) (enumerate arr)))))
      (deftag mapp [f] `(fn[arr] (list (mapp ~f arr))))
      (deftag filterp [f] `(fn[arr] (list (filterp ~f arr)))))
  (do "lambda"
      (deftag map [f] `(fn[arr] (list (map ~f arr))))
      
      (deftag filter [f] `(fn[arr] (list (filter ~f arr))))
      
      (defn filter-or-keep[arr f] (setv filtered (list (filter f arr))) (if filtered filtered arr))
      (defn r-filter[condition? item &optional [key None]]
        (setv res [])
        (if (condition? item) (res.append item))
        (cond [(in (type item) [list tuple]) (for [elem item] (setv r (r-filter condition? elem)) (if r (+= res r)))]
              [(in (type item) [dict]) (for [(, k v) (.items item)] (setv r (r-filter condition? v :key k)) (if r (+= res r)))])
        res)
      (deftag r-filter[f]`(fn[arr] (list (r-filter ~f arr))));doubts I have it may be weak
      (defn apply[f &rest args &kwargs kwargs] (f #*args #**kwargs))
      (defn run[f &optional [args []][daemon None]]
        (setv p (mp.Process :target f :args args :daemon daemon))
        (p.start)
        p)
      )
  (do "csv"
      (defn load-csv [fname &optional [key None][delimiter ","]]
        (setv arr (if (os.path.isfile fname) (-> fname (open "r+") (csv.DictReader :delimiter delimiter) list (as-> it (map dict it)) list ) []))
        (setv arr (list (map dict arr)))
        (if key (do (setv obj {}) (for [row arr] (assoc obj (get row key) row)) obj) 
          arr))
      (defn tolist[&rest args] [#*args])
      (defn fieldnames[arr] (-> (+ [] #*(+ [[]] (list (map (fn[x] (-> x (.keys) list) )arr)))) set list))
      (setv *fieldnames* fieldnames)
      (defn write-csv [fname arr &optional [id None][fieldnames None]]
        (setv writer (-> fname (open "w+") (csv.DictWriter :fieldnames (if fieldnames fieldnames (*fieldnames* arr))) ))
        (writer.writeheader)
        (for [row arr] (writer.writerow row)))
      (defn write-csv-add [fname arr &kwargs kwargs] (as-> fname it (load-csv it) (+ (list it) (list 	arr)) (write-csv fname it #**kwargs)))
      (defn write-txt [name txt] (-> name (open "w+") (.write txt)))
      (defn write-txt-add [name txt] (-> name (open "a+") (.write txt)))
      (defn read-txt [name] (-> name (open "r+") (.read)))
      (setv load-txt read-txt))
  (do "json"
      (defn load-json[fname] (-> fname (open "r+") json.load))
      (defn write-json[fname obj] (-> fname (open "w+") (.write (json.dumps obj))))
      (defn pretty[obj] (json.dumps obj :indent 4 :sort_keys True)))
  (do "jsonl"
      (defn jsonl-json[jstr] (as-> jstr it (.split it "\n")(#filter thru it) (.join "," it)  (.format "[{}]" it)))
      (defn jsonl-loads[jstr] (-> jstr jsonl-json json.loads))
      (defn jsonl-load[f] (-> f (.read) jsonl-loads))
      (defn jsonl-dumps[arr] (.join "\n" (list (map json.dumps arr))))
      (defn jsonl-add[fname item] (-> fname (open "a+") (.write (.format "{}\n" (json.dumps item))))))
  (do "typical vars"
      (setv headers {"User-Agent" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}))
  (do "string funcs/pcze"
      (defn from-between[from a b] (-> from (.split a) last (.split b) first))
      (setv between from-between)
      (defn replace [s obj](for [(, k v) (.items obj)] (setv s (.replace s k v))) s)
      (defn trim[s]
        (setv s (-> s (.replace "\r\n" "\n") (.replace "\n" " ")))
        (while (s.endswith " ") (setv s (get s (slice 0 -1))))
        (while (s.startswith " ") (setv s (get s (slice 1 None))))
        (while (in "  " s) (setv s (s.replace "  " " ")))
        s)
      (defn ascii[s &optional [mode "replace"]](-> s (.encode "ascii" mode) (.decode "ascii")))
      (defn leave-only[s approved] (setv res "") (for [c s] (if (in c approved) (setv res (+ res c)))) res)
      (defn dehydrate[s] (-> s trim ascii (.lower) (leave-only "qwertyuiopasdfghjklzxcvbnm")))
      (defn escape [s] (-> s (.replace "\"" "\\\"") (#%(if (in "\"" %1) (.format "\"{}\"") %1 ))))
      (defn only-pcze[s]
        (setv permitted "1234567890 qwertyuiopasdfghjklzxcvbnm.:;/-\\?!"
              permitted (+ permitted "ąćęłńóśźż")
              permitted (+ permitted (.upper permitted)))
        (as-> s it (list it) (filter (fn[c] (in c permitted)) it) (list it) (.join "" it)))
      (defn remove-control[s] (re.sub "r'\p{C}'" "" s))
      (defn json_quotes_single_to_double[j] (-> j  (replace {"{'" "{\"" "':" "\":" ", '" ", \"" ": '" ": \"" "'}" "\"}" "'," "\"," "']" "\"]" "['" "[\""})))
      (setv json-q-qq json_quotes_single_to_double)
      
      (defn start-same [a b]
        (setv limit (min (len (str a)) (len (str b))))
        (= (get (str a) (slice 0 limit)) (get (str b) (slice 0 limit))))
      (defn short-ean[ean] 
        (if (-> ean str (.replace "." "") (.isdigit))
          (do 
            (setv ean (-> ean float round))
            (while (= 0 (% ean 10)) (setv ean (/ ean 10)))
            (int ean))
          ean))
      (defn same-ean [a b] (start-same (short-ean a) (short-ean b)))
      )
  (do "selectors" 
      
      (defn split-arr[arr &optional [rate 2][from-end False]]
        (if from-end (#map (fn[x] (list (reversed x))) (split-arr (list (reversed arr)) rate))
          (cond [(= 0 (len arr)) [[] []] ]
                [(= 1 (len arr)) [[(first arr)] []]]
                [True (do (setv part (int (* (len arr) rate)))
                          [(get arr (slice 0 part)) (get arr (slice part None))] 
                          )])))
      (defn get-mass[obj fields] (setv res {}) (for [field fields] (if (in field obj) (assoc res field (get obj field)))) res)
      (defn select [arr fields] (list (map (fn[obj] (get-mass obj fields)) arr)))
      
      
      (defn first-that [arr f] (for [elem arr] (if (f elem) (return elem))) None)
      (defmacro last-that [arr f] `(first-that (reversed ~arr) ~f))
      (defn distinct [arr f] (setv res {}) (for [row arr] (assoc res (f row) row)) res)
      (defn get-as[what structure]
        (setv obj {})
        (for [(, k v) (.items structure)]
          (assoc obj k (get what v)))
        obj)
      ; (defn left-join)
      (defn sum-by[arr key]
        (setv sum 0)
        (for [row arr] (+= sum (key row)))
        sum)
      (defn pareto[data coeff key]
        (setv data (sorted data :key key :reverse True))
        
        (setv total (sum-by data key))
        
        
        (for [i (range 1 (len data))]
          (setv sub-data (get data (slice 0 i)))
          (setv sub-total (sum-by sub-data key))
          (if (> sub-total (* coeff total))
            (return sub-data))))
      (defn unique[arr &optional[key None]] (if key 
                                              (do
                                                (setv obj {})
                                                (for [elem arr]
                                                  (assoc obj (key elem) elem))
                                                (.values obj))
                                              (-> arr set list)))
      (defn thru[x] x)
      (defn condense[obj &optional [key thru][value thru][operator +]]
        (if obj 
          (do
            (setv condense-res {})
            (for [(, k v) (.items obj)]
              (setv k (key k)
                    v (value v))
              (if (in k condense-res) (assoc condense-res k (operator (get condense-res k) v)) (assoc condense-res k v)))
            condense-res)
          {}))
      (setv group condense)
      (defn apply-to-chunks[f arr size &optional [process thru]] "rework it - [[] []]"
        (setv buffer [] results []) 
        (while arr
          (buffer.append (arr.pop))
          (if (or (>= (len buffer) size) (not arr)) (do (results.append (f buffer))(setv buffer []))))
        
        (process results))
      (defn chunks[arr size &optional [mode list]]
        (setv res [] buffer [] last-i (- (len arr) 1))
        (for [(, i item) (enumerate arr)]
          (buffer.append item)
          (if (or (>= (len buffer) size) (= i last-i)) (do (res.append (mode buffer)) (setv buffer [])))
          )
        (mode res))
      (defn col[arr c] (list (map (fn[x] (get x c)) arr)))
      (defn cols[arr cs] (list (map (fn[x] (list (map (fn[c] (get x c)) cs))) arr)))
      )
  (do "modern art"
      (deftag whatever[expr] `(do ~expr True)))
  
  
  )

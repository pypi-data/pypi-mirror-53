(import hashlib cloudpickle requests math [anarcute[*]] asyncio aiohttp
        os psutil [pegasi.req[*]]  base64)



(defn mem[] (-> os (.getpid) psutil.Process (.memory-info) (. rss)))
(defn dumps[x &optional[encoding "latin1"]] (-> x cloudpickle.dumps (.decode encoding)))
(defn loads[x &optional[encoding "latin1"]] (-> x (.encode encoding) cloudpickle.loads))
(defn hash[key]
  (-> key (.encode "utf-8") hashlib.sha224 (.hexdigest)))
(defclass Dash[object]
  
  (defn --init--[self key &optional [api "http://0.0.0.0:8080/cloudpickle/"]]
    
    (setv self.key key
          
          self.api api
          self.hash (hash key)
          ))
  (defn loads[self x &rest args &kwargs kwargs] (loads x #*args #**kwargs))
  (defn dumps[self x &rest args &kwargs kwargs] (dumps x #*args #**kwargs));decide out or in
  
  
  
  
  (defn legit[self] (self.run (fn[] {"code" 200 "status" "OK"})))
  (defn run[self &optional [f thru] [args []] [kwargs {}][star True][pickled False] [load False] [save False][test False][requirements None]] 
    (do 
      (setv f (if pickled f (self.dumps f)))
      (setv r (-> (requests.post self.api :json {"f" f "args" (self.dumps (if star args [args])) "kwargs" (self.dumps kwargs)
                                                 "save" save "load" load "test" test "requirements" None
                                                 "hash" self.hash}) 
                  ))
      (try (loads r.text) (except[Exception] r.text))
      
      ))
  (defn save[self f name] (self.run f :save name :test True))
  (defn load[self name] (self.run None :load name :test True))
  
  (defn map[self f args &optional [processes 80] [star False][requirements []] [load False] [save False][test False]]
    (if (and processes (> (len args) processes))
      (do (+ (self.map f (get args (slice 0 processes)) processes star requirements)
             (self.map f (get args (slice processes None)) processes star requirements)))
      (do (setv f (self.dumps f))
          (setv urls (* (len args) [self.api])
                params (list (map (fn[a]{"f" f "args" (self.dumps (if star a [a]))
                                         "hash" self.hash "requirements" (self.dumps requirements)
                                         "save" save "load" load "test" test}) args)))
          
          (setv r (get_map urls :json params))
          (list (map (fn[x](try (loads x) (except[Exception]{"status" "error" "message" x}))) r)))))
  
  
  
  
  
  
  (defn *map[self &rest args &kwargs kwargs] (self.map #*args #**kwargs :star True))
  (setv starmap *map)
  (defn dfilter[self f arr &rest args &kwargs kwargs]
    (setv res (self.map f arr #*args #**kwargs))
    (as-> (list (zip arr res)) it (filter last it) (map first it) (list it)))
  (defn ffilter[self &rest args &kwargs kwargs] (self.run (fn[](self.dfilter #*args #**kwargs))))
  (defn filter[self &rest args &kwargs kwargs] (self.ffilter #*args #**kwargs))
  (defn eep[self &optional[e 5]] (setv sound (.format "{}{}" (* e "e") "p")) (print sound) sound))

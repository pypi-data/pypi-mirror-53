(import [cytoolz [pipe]])


(defn str? [x]
  (isinstance x str))


(defn dict? [x]
  (isinstance x dict))


(defn valmap [value-fn dictionary]
  (dfor [k v] (.items dictionary) [k (value-fn v)]))


(defn $ [&rest args &kwargs kwargs]
  (fn [some-fn] (some-fn #* args #** kwargs)))


(defn lmap [value-fn seq]
  (list (map value-fn seq)))


(defn curry [some-fn &rest args]
  (fn [&rest rest-args] (some-fn #* args #* rest-args)))


(setv thread pipe)

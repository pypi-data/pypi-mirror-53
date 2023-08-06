(require [hy.contrib.walk [let]])

(import [numpy :as np])
(import [pandas :as pd])
(import [cytoolz [merge]])

(import [hyfive.utils [str? lmap curry]])


(defn op [column] (:op column))


(defn alias [column] (:alias column))


(defn args [column] (:args column))


(defn as [column new-alias]
  (merge (col column) {:alias (str new-alias)}))


(defn str-sexp [&rest strings]
  (let [joined (.join " " (map str strings))]
    (+ "(" joined ")")))


(defn lit [value]
  {:op    "literal"
   :alias (str value)
   :args  [value]})


(defn str-to-col [col-name]
  {:op    "generic"
   :alias col-name
   :args  []})


(defn col [collable]
  (cond [(col? collable) collable]
        [(str? collable) (str-to-col collable)]
        [:else           (lit collable)]))


(defn col? [candidate]
  (and (isinstance candidate dict)
       (in :op    candidate)
       (in :alias candidate)
       (in :args  candidate)))


(defn run-col [dataframe column]
  (let [col-op    (op column)
        col-alias (alias column)
        col-args  (args column)
        run       (curry run-col dataframe)]
    (cond [(= col-op "literal") (pd.Series (* col-args (len dataframe)))]
          [(= col-op "generic") (get dataframe col-alias)]
          [:else                (col-op #* (lmap run col-args))])))


(defn add [&rest columns]
  (let [columns (lmap col columns)
        aliases (lmap alias columns)]
    {:op     +
     :alias  (str-sexp "add" #* aliases)
     :args  columns}))


(defn mul [&rest columns]
  (let [columns (lmap col columns)
        aliases (lmap alias columns)]
    {:op     *
     :alias  (str-sexp "mul" #* aliases)
     :args  columns}))


(defn mod [dividend divisor]
  (let [dividend  (col dividend)
        divisor   (col divisor)]
    {:op     %
     :alias  (str-sexp "mod" (alias dividend) (alias divisor))
     :args   [dividend divisor]}))


(defn eq? [left right]
  (let [left  (col left)
        right (col right)]
    {:op     =
     :alias  (str-sexp "eq?" (alias left) (alias right))
     :args   [left right]}))


(defn if-col [predicate then-col else-col]
  (let [predicate  (col predicate)
        then-col   (col then-col)
        else-col   (col else-col)]
    {:op     np.where
     :alias  (str-sexp "if"
               (alias predicate)
               (alias then-col)
               (alias else-col))
     :args   [predicate then-col else-col]}))


(defn cond-col [&rest cond-val-pairs]
  (assert (all (map (fn [x] (= (len x) 2)) cond-val-pairs))
          "Expecting a list of pairs as arguments of hf.when.")
  (reduce add-condition (reversed cond-val-pairs) (lit np.nan)))


(defn add-condition [previous-col next-col]
  (let [predicate (col (first next-col))
        next-col  (col (second next-col))]
    (if-col predicate next-col previous-col)))


(defn is-in [column values]
  (let [column (col column)]
    {:op     (fn [xs] (np.isin xs values))
     :alias  (str-sexp "is-in" (alias column) values)
     :args   [column]}))


(defn single-arg-fn [op-fn op-name column]
  (let [column (col column)]
   {:op     op-fn
    :alias  (str-sexp op-name (alias column))
    :args   [column]}))


(defn min [column] (single-arg-fn np.min "min" column))


(defn mean [column] (single-arg-fn np.mean "mean" column))


(defn std [column] (single-arg-fn np.std "std" column))


(defn max [column] (single-arg-fn np.max "max" column))


(defn sum [column] (single-arg-fn np.sum "sum" column))


(setv rename as)

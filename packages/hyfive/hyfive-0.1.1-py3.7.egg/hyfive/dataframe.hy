(require [hy.contrib.walk [let]])

(import [collections [namedtuple]])

(import [pandas :as pd])

(import [hyfive.column :as hc])
(import [hyfive.utils [str? lmap valmap $]])


(defn ensure-fn [candidate]
  (cond [(hc.col? candidate)  (fn [df] (hc.run-col df candidate))]
        [(callable candidate) candidate]
        [:else                (fn [df] candidate)]))


(defn select [dataframe &rest columns]
  (cond [(all-str? columns) (get dataframe (list columns))]
        [(all-col? columns) (select-cols dataframe columns)]
        [:else
          (raise (KeyError
                   "hf.select expects all col names or all HyFive cols."))]))


(defn select-cols [dataframe columns]
  (let [aliases (lmap hc.alias columns)
        col-map (dict (zip aliases columns))]
    (-> dataframe
        (with-columns col-map)
        (select #* aliases))))


(defn filter [dataframe predicate]
  (let [predicate (ensure-fn predicate)]
    (.reset_index (get dataframe (predicate dataframe)))))


(defn with-column [dataframe col-name col-fn]
  (let [col-fn (ensure-fn col-fn)]
    (.assign dataframe #** {col-name (col-fn dataframe)})))


(defn with-columns [dataframe new-col-map]
  (let [apply-to-df (comp ($ dataframe) ensure-fn)
        applied-map (valmap apply-to-df new-col-map)]
    (.assign dataframe #** applied-map)))


(defn with-column-renamed [dataframe old-name new-name]
  (if (in new-name dataframe)
    (setv dataframe (drop-columns dataframe new-name)))
  (.rename dataframe :columns {old-name new-name}))


(defn with-columns-renamed [dataframe rename-map]
  (.rename dataframe :columns rename-map))


(defn drop-columns [dataframe &rest col-names]
  (.drop dataframe :columns (list col-names)))


(defn join [dataframe right &kwargs kwargs]
  (.merge dataframe right #** kwargs))


(defn group-by [dataframe &rest by]
  (let [by (if (= (len by) 1)
               by
               (list by))]
    (.groupby dataframe by)))


(defn agg [dataframe &rest args]
  (if (and (= (len args) 1)
           (not (hc.col? (first args))))
      (agg-by-map dataframe (first args))
      (let [fn-map (dfor col args [(hc.alias col) col])]
        (agg-by-map dataframe fn-map))))


(defn agg-by-map [dataframe fn-map]
  (let [fn-map (valmap ensure-fn fn-map)]
    (-> dataframe
        (.apply (fn [group-df]
                  (setv applied-map (valmap ($ group-df) fn-map))
                  (pd.Series applied-map)))
        (.reset-index))))


(defn order-by [dataframe by &optional [desc False]]
  (-> dataframe
    (.sort-values :by by :ascending (not desc))
    (.reset-index :drop True)))


(defn all-str? [candidates] (all (map str? candidates)))


(defn all-col? [candidates] (all (map hc.col? candidates)))


(setv groupby group-by)

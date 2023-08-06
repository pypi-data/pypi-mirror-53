(require [hy.contrib.walk [let]])

(import [hyfive :as hf])


(defn should-curry [fn-name]
  (in fn-name ["select"
               "filter"
               "with_column"
               "with_columns"
               "with_column_renamed"
               "with_columns_renamed"
               "drop_columns"
               "join"
               "group_by"
               "groupby"
               "agg"
               "order_by"]))


(defn curry-dataframe [dataframe-fn]
  (fn [&rest args &kwargs kwargs]
    (fn [dataframe] (dataframe-fn dataframe #* args #** kwargs))))


(.update (locals)
  (dfor [fn-name candidate-fn] (.items (vars hf))
    [fn-name (if (should-curry fn-name)
               (curry-dataframe candidate-fn)
               candidate-fn)]))

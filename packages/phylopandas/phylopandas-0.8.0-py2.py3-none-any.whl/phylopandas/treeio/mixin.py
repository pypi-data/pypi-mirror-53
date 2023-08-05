

class DataFrameTreeMethods:
    """Tree operations
    """

    def prune(self, label):
        df = self._data
        tree = df.phylo.to_dendropy()

        obj = df.row_by_value(label)
        


        # Slice out matching rows
        slice = df.loc[df.label == str(label)]
        row = slice.iloc[0]


methods = {
            "Fill with a specific object": "{df}['{col}'].fillna('{x}', inplace=True)",
            "Forward fill": "{df}['{col}'].ffill(inplace=True)",
            "Backward fill": "{df}['{col}'].bfill(inplace=True)",

            "Delete rows": "{df}.dropna(subset=['{col}'], inplace=True)",

            "Fill with a specific value": "{df}['{col}'].fillna({x}, inplace=True)",
            "Fill with mean": "{df}['{col}'].fillna({df}['{col}'].mean(), inplace=True)",
            "Fill with median": "{df}['{col}'].fillna({df}['{col}'].median(), inplace=True)",
            "Fill with mode": "{df}['{col}'].fillna({df}['{col}'].mode()[0], inplace=True)",
            "Interpolate": "{df}['{col}'].interpolate(method='{x}', inplace=True)",

            "Fill with a specific date": "{df}['{col}'].fillna(pd.Timestamp('{x}'), inplace=True)",
    }
from sorted_nearest import makewindows
from sorted_nearest import maketiles


def _windows(df, kwargs):

    window_size = kwargs["window_size"]

    idxs, starts, ends = makewindows(df.index.values, df.Start.values,
                                     df.End.values, window_size)

    df = df.reindex(idxs)
    df.loc[:, "Start"] = starts
    df.loc[:, "End"] = ends

    return df


def _tiles(df, kwargs):

    window_size = kwargs["tile_size"]

    idxs, starts, ends = maketiles(df.index.values, df.Start.values,
                                   df.End.values, window_size)

    df = df.reindex(idxs)
    df.loc[:, "Start"] = starts
    df.loc[:, "End"] = ends

    return df

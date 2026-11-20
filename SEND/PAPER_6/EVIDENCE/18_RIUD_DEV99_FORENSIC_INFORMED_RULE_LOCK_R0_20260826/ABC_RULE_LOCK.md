# DEV99 ABC rule lock

The ABC label is a strict timing-order classification recovered from the
DEV99 H99 source. It is not a new classifier and it does not change the
DEV99 map, node, path, or R40 law.

```text
A      if GAP_TIME < T0 < MAX_FLOW
B      if GAP_TIME < MAX_FLOW < T0
C      if MAX_FLOW < GAP_TIME < T0
OTHER  otherwise, including invalid or unavailable ordering
```

No tolerance, <= comparison, imputation, or outcome-dependent exception is
used. Reapplication to SOURCE_ABC_X_H99.csv reproduces 96/96 labels.

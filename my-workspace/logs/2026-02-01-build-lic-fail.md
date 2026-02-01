# Session: 2026-02-01 - Build Failed (License)

## Summary

`./build.sh all` failed at the first Spectre run due to missing license path.

## Error

```
lmStatus: ERROR (LMC-01902): License call failed. The license server search
path is defined as <none>. Can't find license file.
```

## Next Steps

- Configure license environment (CMC Cloud provides this on the remote host)
- Re-run `./build.sh all` to verify Level 4/3 truth tables

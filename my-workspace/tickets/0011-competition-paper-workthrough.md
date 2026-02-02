# 0011: Competition LaTeX Workthrough Paper

**Status:** In Progress (source-complete, build-tool constrained)
**Priority:** High
**Created:** 2026-02-02

## Description

Create a video-aligned LaTeX technical workthrough that shows raw electrical
evidence, implementation artifacts, and reproducible commands in one paper.

## Tasks

- [x] Define paper structure and required evidence sections
- [x] Build raw-data helper parser for sweep and first-spike summaries
- [x] Author LaTeX paper with dark-theme unsmoothed plots from CSV data
- [x] Add paper build script and README
- [ ] Compile PDF in an environment with LaTeX engine installed

## Acceptance Criteria

1. Paper source is complete and self-contained in repo
2. Figures use sampled data points (no smoothing)
3. Tables cover analog metrics, sweep envelope, and flow status
4. Build process is scripted and reproducible once LaTeX engine is available

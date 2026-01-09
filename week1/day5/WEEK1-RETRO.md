# WEEK 1 - RETRO

This document summarizes my learnings, mistakes, and fixes from **Week 1 (Day 1–Day 5)**. The focus was not just completing tasks, but understanding how systems, Node.js, Git, HTTP, and automation actually behave in practice.

---

## DAY 1 — System Reverse Engineering & Terminal Mastery

### What I Did
- Inspected OS version, shell, PATH variables, Node binary path, and npm global path using terminal commands only.
- Installed NVM and switched between Node LTS and latest versions.
- Created `introspect.js` to print system details such as OS, CPU cores, memory, uptime, user, and Node path.
- Benchmarked **Buffer vs Stream** file reading using a large file and logged performance metrics.

### What I Learned
- PATH order directly affects which Node binary is executed.
- Streams process data incrementally and are safer for large files.
- Measuring performance requires consistent runs and controlled conditions.

### What Broke / Challenges
- I initially misinterpreted PATH output and couldn’t understand why `which node` pointed to a different binary after installing NVM.
- Memory readings were inconsistent at first because garbage collection timing affected results.
- Creating a truly large test file required trial and error.

---

## DAY 2 — Node CLI App, Concurrency & Large Data Processing

### What I Did
- Generated a corpus file with more than 200,000 words.
- Built a CLI tool `wordstat.js` with multiple flags.
- Implemented chunk-based processing and parallel execution.
- Benchmarked concurrency levels (1, 4, 8) and logged performance.

### What I Learned
- CLI argument parsing must handle invalid or missing inputs gracefully.
- Concurrency has overhead; higher parallelism is not always faster.
- File chunking can introduce subtle bugs.

### What Broke / Challenges
- Words were getting split across chunks, causing incorrect counts initially.
- Increasing concurrency increased memory usage and sometimes slowed execution.
- Debugging parallel execution was harder than expected because logs were interleaved.

---

## DAY 3 — Git Mastery 

### What I Did
- Created multiple commits and intentionally introduced a bug.
- Used `git bisect` to find the exact faulty commit.
- Fixed the bug and reverted it using `git revert`.
- Practiced stash workflows and resolved merge conflicts using two clones.

### What I Learned
- `git bisect` is extremely effective for isolating regressions.
- `git revert` preserves history and is safer in collaborative workflows.
- Merge conflicts are manageable if approached calmly.

### What Broke / Challenges
- During merge conflict resolution, I almost overwrote one side’s changes.
- I initially confused `reset` and `revert` and had to redo the exercise.
- Stash usage felt risky until I understood how to safely reapply changes.

---

## DAY 4 — HTTP / API Forensics

### What I Did
- Used `nslookup` and `traceroute` to analyze DNS resolution and routing.
- Inspected HTTP traffic using `curl -v`.
- Modified headers such as `User-Agent` and `Authorization`.
- Tested ETag-based caching with `If-None-Match`.
- Built a Node.js HTTP server with `/echo`, `/slow`, and `/cache` endpoints.

### What I Learned
- HTTP headers directly control caching, authentication, and client behavior.
- `304 Not Modified` responses save bandwidth and time.
- Network tools expose how requests actually travel.

### What Broke / Challenges
- `curl -v` output was overwhelming and hard to interpret initially.
- I misunderstood why responses were cached until I carefully inspected headers.
- Implementing correct cache headers required multiple test iterations.

---

## DAY 5 — AUTOMATION & MINI-CI PIPELINE

### What I Did
- Wrote `validate.sh` to enforce project structure, validate JSON, and log results.
- Integrated ESLint and Prettier to enforce formatting.
- Added Husky pre-commit hooks to block bad commits.
- Created timestamped build artifacts including source code and logs.
- Generated SHA checksums for build integrity.
- Scheduled the pipeline using cron.

### What I Learned
- Automation catches mistakes before they enter the repository.
- Pre-commit hooks enforce discipline without manual effort.
- CI concepts can be applied locally with simple tools.

### What Broke / Challenges
- I was confused when ESLint and Prettier passed but commits were still blocked by Husky.
- Prettier warnings felt unclear until I understood `--check` vs `--write`.
- I accidentally committed `node_modules`, creating a massive commit and realizing the importance of `.gitignore`.
- Cron setup was confusing at first because pressing Enter auto-selected the default editor, which I didn’t realize immediately.
- Husky deprecation warnings were alarming until I understood they were informational.

---

## Overall Takeaways

- I learned to deeply understand the system through the terminal, measure real performance instead of guessing, and treat Git mistakes as recoverable events rather than failures.
- Most importantly, setting up automation (linting, validation, pre-commit hooks, and cron) showed me that good engineering relies on systems that prevent errors, not manual checks.
- This experience made me more confident, structured, and production-oriented as a developer.


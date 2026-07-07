Investigate why TC-08 (adversarial non-native English) times out in the eval harness.

The test case input is at `tests/superset/inputs/tc08-adversarial.txt` — a 5-line job application email written by a non-native English speaker.

The eval harness at `tests/superset/evaluate-superset.sh` runs `opencode run` with the skill at `skills/ai-output-humanizer/SKILL.md` and captures output. At k=5, TC-08 consistently times out (exceeds 900s) while other test cases complete in ~60s each.

Your job:
1. Read the skill SKILL.md and the test input.
2. Run `opencode run` manually with the skill + TC-08 input and time it.
3. If it hangs, identify what causes the delay — is the agent stuck in a loop? Is the non-native handling section causing excessive analysis? Is the output too long?
4. Report findings in `FINAL_OUTPUT.md` with:
   - Root cause of the timeout
   - Whether it's a skill instruction problem, a test input problem, or a harness problem
   - Specific fix recommendation (if skill-related, include the exact text to change)

Use `--model ollama-cloud/deepseek-v4-flash:cloud` for the test run. Time the invocation with `time` or `gdate`.

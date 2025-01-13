---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: Lerbaek

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Response body**
If applicable, enable debug logging through the [integration configuration](https://my.home-assistant.io/redirect/integration/?domain=copenhagen_trackers) or by adding this snippet to your configuration.yaml:

```yaml
logger:
  default: info
  logs:
    custom_components.copenhagen_trackers: debug
```

After reloading the tracker configuration, please retrieve the response body from the full [logs](https://my.home-assistant.io/redirect/logs/?) after `Data fetched: `).

Feel free to redact any sensitive information - The main structure is what's interesting.

**Additional context**
Add any other context about the problem here.

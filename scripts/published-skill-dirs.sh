#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"

ruby -rjson -e '
repo = File.expand_path(ARGV.fetch(0))
manifest = File.join(repo, ".claude-plugin", "plugin.json")
data = JSON.parse(File.read(manifest))
skills = data.fetch("skills")

abort "manifest field .skills must be an array" unless skills.is_a?(Array)

skills.each do |entry|
  abort "manifest skill entry must be a string: #{entry.inspect}" unless entry.is_a?(String)

  path = File.expand_path(entry, repo)
  unless path == repo || path.start_with?(repo + File::SEPARATOR)
    abort "manifest skill escapes repo: #{entry}"
  end

  skill_md = File.join(path, "SKILL.md")
  abort "manifest skill missing SKILL.md: #{entry}" unless File.file?(skill_md)

  puts path
end
' "$REPO"

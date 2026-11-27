"use strict";

const REPO_MARKDOWN_FORM = "`<path to a .md file> in <owner>/<repo>`";

const parseRepoMarkdown = (value) => {
  const match = typeof value === "string" && value.match(/^([^\s\\:]+\.md) in ([\w.-]+)\/([\w.-]+)$/);
  if (!match) return null;
  const [, file, owner, repo] = match;
  if (file.startsWith("/") || file.split("/").includes("..") || [owner, repo].some((name) => /^\.+$/.test(name))) return null;
  return { file, owner, repo };
};

module.exports = { REPO_MARKDOWN_FORM, parseRepoMarkdown };

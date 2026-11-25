"use strict";

const API = "https://api.higgsfield.ai";
const QUOTED_BODY_CHARS = 200; // #583 guess
const MAX_TRIES = 3; // #583 guess
const FIRST_RETRY_WAIT_MS = 2000; // #583 guess
const RETRY_DEADLINE_MS = 60 * 1000; // #590 guess
const HINTS = {
  401: " (check HIGGSFIELD_API_KEY)",
  403: " (the balance is too low: top up at open.higgsfield.ai)",
};
class RefusalError extends Error {
  constructor(message, retryable) {
    super(message);
    this.retryable = retryable;
  }
}

class ApiError extends RefusalError {
  constructor(message, status) {
    super(message, status >= 500);
    this.name = "ApiError";
    this.status = status;
  }
}

function originOf(url) {
  try {
    return new URL(url).origin;
  } catch {
    return "a URL that does not parse";
  }
}

class OffApiUrlError extends RefusalError {
  constructor(method, url) {
    super(`${method} to ${originOf(url)} was not sent: only a string starting ${API}/ is`, false);
    this.name = "OffApiUrlError";
    this.url = url;
  }
}

// #583
async function call(ctx, method, url, { body, headers = {}, signal } = {}) {
  // #588
  if (typeof url !== "string" || !url.startsWith(`${API}/`)) throw new OffApiUrlError(method, url);
  const response = await ctx.fetch(url, {
    method,
    headers: { Authorization: `Key ${ctx.credentials}`, ...(body ? { "Content-Type": "application/json" } : {}), ...headers },
    body: body ? JSON.stringify(body) : undefined,
    redirect: "error",
    signal,
  });
  const text = await response.text();
  let json;
  try {
    json = JSON.parse(text);
  } catch {
    json = undefined;
  }
  if (!response.ok) {
    const detail = json?.detail === undefined ? text.slice(0, QUOTED_BODY_CHARS) : typeof json.detail === "string" ? json.detail : JSON.stringify(json.detail);
    throw new ApiError(`${method} ${new URL(url).pathname} answered ${response.status}: ${detail}${HINTS[response.status] ?? ""}`, response.status);
  }
  return json;
}

// #583, #587
async function withRetry(ctx, method, url, request = {}) {
  const deadline = ctx.now() + ctx.retryDeadlineMs;
  for (let tries = 1; ; tries++) {
    const tryMs = Math.ceil(Math.min(deadline - ctx.now(), ctx.retryDeadlineMs / MAX_TRIES));
    const signal = ctx.timeout(Math.max(0, tryMs));
    try {
      return await call(ctx, method, url, { ...request, signal });
    } catch (thrown) {
      const error = signal.aborted && thrown === signal.reason ? new Error(`${method} ${new URL(url).pathname} gave no answer within ${tryMs / 1000} s, its try's share of the ${ctx.retryDeadlineMs / 1000} s retry deadline`, { cause: thrown }) : thrown;
      const transient = !(error instanceof RefusalError) || error.retryable;
      const wait = FIRST_RETRY_WAIT_MS * 2 ** (tries - 1);
      if (!transient || tries >= MAX_TRIES || ctx.now() + wait >= deadline) {
        if ((transient || tries > 1) && error instanceof Error) error.mayHaveReached = true;
        throw error;
      }
      await ctx.sleep(wait);
    }
  }
}

module.exports = { API, RETRY_DEADLINE_MS, RefusalError, withRetry };

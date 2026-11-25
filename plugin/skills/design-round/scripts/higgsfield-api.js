"use strict";

const API = "https://api.higgsfield.ai";
const QUOTED_BODY_CHARS = 200; // #583 guess
const MAX_TRIES = 3; // #583 guess
const FIRST_RETRY_WAIT_MS = 2000; // #583 guess
const RETRY_DEADLINE_MS = 60 * 1000; // #590 guess
// https://www.rfc-editor.org/rfc/rfc9110#section-15.5.9 https://www.rfc-editor.org/rfc/rfc6585#section-4
const ASK_AGAIN_STATUSES = new Set([408, 429]);
// A 429 creates and charges nothing: https://docs.higgsfield.ai/docs/concepts/rate-limits.md
const UNCHARGED_ASK_AGAIN_STATUSES = new Set([429]);
// Seconds, as https://docs.higgsfield.ai/docs/api-reference/headers.md gives it
const RETRY_AFTER_SECONDS = /^\d+$/;
const HINTS = {
  401: " (check HIGGSFIELD_API_KEY)",
  403: " (the balance is too low: top up at open.higgsfield.ai)",
  429: " (rate limited: rerun later)",
};
class RefusalError extends Error {
  constructor(message, retryable) {
    super(message);
    this.retryable = retryable;
  }
}

class ApiError extends RefusalError {
  constructor(message, status, retryAfterMs) {
    super(message, status >= 500 || ASK_AGAIN_STATUSES.has(status));
    this.name = "ApiError";
    this.status = status;
    this.retryAfterMs = retryAfterMs;
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
    const retryAfter = response.headers.get("retry-after")?.trim();
    const retryAfterMs = RETRY_AFTER_SECONDS.test(retryAfter ?? "") ? Number(retryAfter) * 1000 : undefined;
    throw new ApiError(`${method} ${new URL(url).pathname} answered ${response.status}: ${detail}${HINTS[response.status] ?? ""}`, response.status, retryAfterMs);
  }
  return json;
}

const isTransient = (error) => !(error instanceof RefusalError) || error.retryable;
const isUncharged = (error) => error instanceof RefusalError && (!error.retryable || UNCHARGED_ASK_AGAIN_STATUSES.has(error.status));

// #583, #587, #591
async function withRetry(ctx, method, url, request = {}) {
  const deadline = ctx.now() + ctx.retryDeadlineMs;
  let mayHaveReached = false;
  let waitedOutRetryAfter = false;
  for (let tries = 1; ; tries++) {
    const tryMs = Math.ceil(Math.min(deadline - ctx.now(), ctx.retryDeadlineMs / MAX_TRIES));
    const signal = ctx.timeout(Math.max(0, tryMs));
    try {
      return await call(ctx, method, url, { ...request, signal });
    } catch (thrown) {
      const error = signal.aborted && thrown === signal.reason ? new Error(`${method} ${new URL(url).pathname} gave no answer within ${tryMs / 1000} s, its try's share of the ${ctx.retryDeadlineMs / 1000} s retry deadline`, { cause: thrown }) : thrown;
      mayHaveReached ||= !isUncharged(error);
      const backoff = FIRST_RETRY_WAIT_MS * 2 ** (tries - 1);
      const wait = Math.max(backoff, error?.retryAfterMs ?? 0);
      waitedOutRetryAfter ||= wait > backoff;
      const keptForTheTry = waitedOutRetryAfter ? ctx.retryDeadlineMs / MAX_TRIES : 0;
      if (!isTransient(error) || tries >= MAX_TRIES || ctx.now() + wait + keptForTheTry >= deadline) {
        if (mayHaveReached && error instanceof Error) error.mayHaveReached = true;
        throw error;
      }
      await ctx.sleep(wait);
    }
  }
}

module.exports = { API, QUOTED_BODY_CHARS, RETRY_DEADLINE_MS, RefusalError, isTransient, withRetry };

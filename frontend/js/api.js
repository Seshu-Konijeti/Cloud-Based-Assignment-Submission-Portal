/**
 * api.js
 * Thin wrapper around fetch() for talking to the Flask REST API.
 * The JWT is stored in localStorage for demo simplicity -- in a
 * production-hardened build you'd prefer an httpOnly cookie to
 * reduce XSS token-theft risk.
 */
const API_BASE = "http://localhost:5000/api";

function getToken() {
  return localStorage.getItem("access_token");
}

function setToken(token) {
  localStorage.setItem("access_token", token);
}

function clearSession() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("user");
}

function getUser() {
  const raw = localStorage.getItem("user");
  return raw ? JSON.parse(raw) : null;
}

async function apiRequest(path, { method = "GET", body = null, isForm = false } = {}) {
  const headers = {};
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (!isForm && body) headers["Content-Type"] = "application/json";

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: isForm ? body : body ? JSON.stringify(body) : null,
  });

  let data;
  try {
    data = await res.json();
  } catch (e) {
    data = {};
  }

  if (!res.ok) {
    const err = new Error(data.message || "Request failed");
    err.status = res.status;
    err.payload = data;
    throw err;
  }
  return data;
}

function requireAuth(allowedRoles) {
  const user = getUser();
  const token = getToken();
  if (!token || !user) {
    window.location.href = "login.html";
    return null;
  }
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    alert("You are not authorized to view this page.");
    window.location.href = "login.html";
    return null;
  }
  return user;
}

function logout() {
  clearSession();
  window.location.href = "login.html";
}
